# Ros Client
import rospy

# Standard Python Libraries
import threading
import os
import time

# Messages
from geometry_msgs.msg import Twist

# Third Party Libraries
from flask import Flask, request, Response
from pi_drone_server.html import html
from pi_drone_server.camera import Camera

# Globals
current_speed = 0
current_turn = 0
ping_time = 0
write_event = threading.Event()
app = Flask(__name__)

# Constants
TIMEOUT = 1.5 # Seconds

direction = rospy.Publisher("robot_twist", Twist, queue_size=10)

@app.route('/')
def view():
    return html


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/control")
def control():
    global direction, current_speed, current_turn, write_event
    # Decode Speed
    if 'speed' in request.args and int(request.args["speed"]) != current_speed:
        current_speed = request.args["speed"]
    else:
        current_speed = 0
    # Decode Turn
    if 'turn' in request.args and int(request.args["turn"]) != current_turn:
        current_turn = request.args["turn"]
    else:
        current_turn = 0

    # Signal To ros_thread That New Directions Have Been Received
    write_event.set()

    # Return Code 204
    return ('', 204)


@app.route("/ping")
def ping():
    global ping_time
    ping_time = time.time()
    return ('', 204)


def timeout_thread():
    global ping_time, current_speed, current_turn, write_event, TIMEOUT
    time.sleep(1) # We need to wait for the rospy node to initialize before running.
    while not rospy.is_shutdown():
        if (time.time() - ping_time) > TIMEOUT:
            current_speed = 0
            current_turn = 0
            write_event.set()
        time.sleep(0.1)


def ros_thread():
    global current_speed, current_turn, write_event, direction
    rospy.init_node('pi_drone_server', disable_signals=True)

    while not rospy.is_shutdown():
        write_event.wait()
        msg = Twist()
        msg.linear.x = float(current_speed)
        msg.angular.z = float(current_turn)
        direction.publish(msg)
        write_event.clear()


def pi_drone_server():
    """Executable"""
    threading.Thread(target=ros_thread).start()
    threading.Thread(target=timeout_thread).start()
    app.run(host="0.0.0.0", threaded=True)

