# Ros Client
import rospy

# Standard Python Libraries
import threading
import os

# Messages
from geometry_msgs.msg import Twist

# Third Party Libraries
from flask import Flask, request
from pi_drone_server.html import html

# Globals
current_speed = 0
current_turn = 0
app = Flask(__name__)

threading.Thread(target=lambda: rospy.init_node('pi_drone_server', disable_signals=True)).start()
direction = rospy.Publisher("robot_twist", Twist, queue_size=10)

@app.route('/')
def view():
    return html


@app.route("/control")
def control():
    global direction, current_speed, current_turn
    # Initialize Message
    msg = Twist()
    msg.linear.x = 0
    msg.angular.z = 0

    # Decode Request
    if 'speed' in request.args and int(request.args["speed"]) != current_speed:
        msg.linear.x = int(request.args["speed"])
    if 'turn' in request.args and int(request.args["turn"]) != current_turn:
        msg.angular.z = int(request.args["turn"])

    # Update Current Speed and Turn
    current_speed = msg.linear.x
    current_turn = msg.angular.z

    # Start a New Thread To Publish The Twist Message
    threading.Thread(target=lambda: direction.publish(msg)).start()

    # Return Code 204
    return ('', 204)


def pi_drone_server():
    """Executable"""
    app.run(host="0.0.0.0")

