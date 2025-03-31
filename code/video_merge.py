import os
import subprocess

# Path to your Downloads folder
downloads_path = os.path.expanduser("~/Downloads")
os.chdir(downloads_path)

# Get and sort .h264 files
h264_files = sorted([f for f in os.listdir() if f.endswith(".h264")])

# Write to list.txt
with open("list.txt", "w") as f:
    for file in h264_files:
        f.write(f"file '{file}'\n")

# Merge .h264 files
subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "merged.h264"])

# Convert to .mp4
subprocess.run(["ffmpeg", "-framerate", "30", "-i", "merged.h264", "-c", "copy", "output.mp4"])

print("🎬 All videos merged and converted to output.mp4")
