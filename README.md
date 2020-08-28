# Pi Drone Server
This package provides a web interface for controlling a robotic drone powered by a Raspberry Pi and equipped with a standard Raspberry Pi Camera.
The web interface provides a live video feed and directional control buttons and is viewable from any browser at your Pi's IP on port 5000. To integrate
this package into your ROS environment, directional messages received from the web interface are posted to the topic [robot_twist](#Topics). 

# Requirements
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [picamera](https://picamera.readthedocs.io/en/release-1.13/)

# Controlling Your Robot
Below the video feed, you will see four button labled "Left", "Forward", "Reverse", "Right". Press a button to post the corresponding direction to 
[robot_twist](#Topics). Press the same button again to stop. For example, if you pressed "Left", "Forward", "Forward" in that order, you would 
turn left, then drive forward, then stop.

# <a name="Topics"></a>Topics
### robot_twist
Encodes the robot's desired direction of motion with a [geometry_msgs/Twist](http://docs.ros.org/melodic/api/geometry_msgs/html/msg/Twist.html) message. 
Linear motion is encoded in msg.linear.x with -1 corresponding to reverse and 1 corresponding to forward while angular motion is encoded in msg.angular.z 
with -1 corresponding to right and 1 corresponding to left.

# Nodes
### pi_drone_server
Provides a web server on port 5000 serving the web interface and video feed. Publishes directions to [/robot_twist](#Topics).
```
rosrun pi_drone_server pi_drone_server
```

# Sources
The code for the video stream was forked from Miguel Grinberg's [flask-video-streaming](https://github.com/miguelgrinberg/flask-video-streaming). 
You can learn more about how this feature was implemented by reading his [article](https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited) 
on the subject.
