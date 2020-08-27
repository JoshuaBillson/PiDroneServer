import rospy
from geometry_msgs.msg import Twist
from flask import Flask, request
import threading
import os

html = """<!DOCTYPE html>
<html lang="en" dir="ltr">

<head>
    <!-- Meta Data -->
    <meta charset="utf-8">
    <meta name="author" content="Joshua Billson">
    <meta name="description" content="Robot Server">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Robot Server</title>
</head>

<body>
<div class="container-fluid my-0 mt-md-3 mx-0 py-0 pt-md-3 px-0 mb-0 pb-0">
    <div class="row align-content-center text-center mx-0">
        <div class="col-10 offset-1 col-md-8 offset-md-2">
            <img class="img img-fluid" src="https://cdn.pixabay.com/photo/2019/11/10/16/47/nature-4616282_1280.jpg"
                 alt="viewport" style="max-height: 80vh;">
        </div>
        <div class="col-12 offset-md-2 col-md-8 py-1 my-1 align-content-center text-center">
            <button onclick="turnLeft()" class="btn btn-dark btn-large py-2 m-2" style="width: 100px;">Left</button>
            <button onclick="forward()" class="btn btn-dark btn-large py-2 m-2" style="width: 100px;">Forward</button>
            <button onclick="backward()" class="btn btn-dark btn-large py-2 m-2" style="width: 100px;">Reverse</button>
            <button onclick="turnRight()" class="btn btn-dark btn-large py-2 m-2" style="width: 100px;">Right</button>
        </div>
    </div>
</div>

<!-- Scripts -->
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

<script>
    let request = new XMLHttpRequest();

    function turnLeft() {
        request.open("GET", "/control?speed=0&turn=1");
        request.send();
    }

    function turnRight() {
        request.open("GET", "/control?speed=0&turn=-1");
        request.send();
    }

    function forward() {
        request.open("GET", "/control?speed=1&turn=0");
        request.send();
    }

    function backward() {
        request.open("GET", "/control?speed=-1&turn=0");
        request.send();
    }
</script>

</body>

</html>"""

app = Flask(__name__)

threading.Thread(target=lambda: rospy.init_node('pi_drone_server', disable_signals=True)).start()
direction = rospy.Publisher("robot_twist", Twist, queue_size=10)

@app.route('/')
def view():
    return html


@app.route("/control")
def control():
    global direction
    speed = 0
    turn = 0
    if 'speed' in request.args:
        speed = int(request.args['speed'])
    if 'turn' in request.args:
        turn = int(request.args['turn'])
    msg = Twist()
    msg.linear.x = speed
    msg.angular.z = turn
    threading.Thread(target=lambda: direction.publish(msg)).start()
    #direction.Publish(msg)
    return ('', 204)


def pi_drone_server():
    """Executable"""
    app.run(host="0.0.0.0")

