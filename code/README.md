# Hermes Rocket Project 🚀

This file contains all the python files that were used the project, in order to create this files the help of ChatGPT was used.

## Contents

- `camery.py` - Is the script for the camera to start recording
- `post_flight_plot.py` - Is the script in order to re watch the telemetry after the flight
- `receive_live2.py` - Is the script for the ground station in this case the macbook I had 
- `send_data3.py` - Is the script for the raspberry pi, specifically for the sensors to work. It needs to be run separately from the camera.py script as most of the libraries can only be used in a virtual environment
- `video_merge.py` - Is the script that merges all the video files and then converts them from .h264 to mp4 
- `flight_simulation.py` - Is the script that simulates the movement of the rocket based on its accelerometer and gyroscope data.
