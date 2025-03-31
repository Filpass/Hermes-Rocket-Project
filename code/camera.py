from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time
import datetime

# Initialize camera
picam2 = Picamera2()
video_config = picam2.create_video_configuration(
    main={"size": (1920, 1080)},
    controls={"FrameRate": 30}
)
picam2.configure(video_config)

encoder = H264Encoder(bitrate=10000000)
picam2.start()

print("Recording camera segments...")

try:
    while True:
        # Generate timestamped filename
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"video_{timestamp}.h264"
        output = FileOutput(filename)

        # Start new recording
        picam2.start_recording(encoder, output)
        print(f"Recording: {filename}")
        
        # Record for 30 seconds
        time.sleep(30)

        # Stop and flush
        picam2.stop_recording()
        print(f"Saved: {filename}")

except KeyboardInterrupt:
    print("Recording interrupted by user.")
finally:
    picam2.close()
