# Pi Drone Server
This package provides a web interface for a robotic drone powered by a raspberry pi equipped with a PiCamera. 
A live video feed and directional control buttons are provided for the user. Directions are published to Topic as a
geometry_msgs/Twist message which can then be used to drive your robot.

# Python Requirements
The package uses Flask for the server backend and picamera for the video feed.
