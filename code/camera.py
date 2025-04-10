from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time
import datetime

# Initialize camera
picam2 = Picamera2()
video_config = picam2.create_video_configuration(
    main={"size": (1280, 720)},  # 720p resolution
    controls={"FrameRate": 30}
)
picam2.configure(video_config)

encoder = H264Encoder(bitrate=10000000)
picam2.start()

print("Recording video...")

# Start recording into a temporary buffer (not saving yet)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"video_{timestamp}.h264"
output = FileOutput(filename)
picam2.start_recording(encoder, output)
print(f"Recording started: {filename}")

try:
    while True:
        # Continue recording until there's a reason to stop, e.g., user interrupt or specific condition
        time.sleep(1)  # Recording is continuous

        # Here you could periodically check if the file needs to be closed or saved.
        # For example, flush data or rotate files every 60 seconds, or some other custom interval
        # without interrupting the video feed. This is for continuous recording.

except KeyboardInterrupt:
    print("Recording interrupted by user.")
finally:
    # Ensure the final file is saved
    picam2.stop_recording()
    print(f"Final recording saved: {filename}")
    picam2.close()
