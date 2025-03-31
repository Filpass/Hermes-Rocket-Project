import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import numpy as np
from math import sqrt, atan2, degrees

# Set up the UDP socket to receive data
HOST = '0.0.0.0'  
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.settimeout(2)

# Initialize data lists
time_data = []
temperature_data = []
altitude_barometric_data = []
altitude_gps_data = []
velocity_data = []
vertical_speed_data = []
acceleration_magnitude_data = []
rotation_rate_data = []
orientation_pitch_data = []
orientation_roll_data = []
orientation_yaw_data = []
latitude_data = []
longitude_data = []
drift_data = []

# Store previous values for calculations
prev_altitude = None
initial_latitude = None
initial_longitude = None
initial_roll = None  # Roll Calibration

# Initialize figure and subplots
fig, axs = plt.subplots(3, 3, figsize=(16, 12))

# Assigning subplots
(ax_temperature, ax_altitude, ax_velocity,
 ax_acceleration, ax_vertical_speed, ax_orientation,
 ax_rotation_rate, ax_drift, _) = axs.flatten()

# Set subplot titles
ax_temperature.set_title("Temperature vs Time")
ax_altitude.set_title("Altitude (Barometric & GPS) vs Time")
ax_velocity.set_title("Velocity vs Time")
ax_acceleration.set_title("Acceleration Magnitude vs Time")
ax_vertical_speed.set_title("Vertical Speed vs Time")
ax_orientation.set_title("Orientation (Pitch, Roll, Yaw) vs Time")
ax_rotation_rate.set_title("Rotation Rate vs Time")
ax_drift.set_title("Rocket Drift vs Time")

# Define plot lines
temperature_line, = ax_temperature.plot([], [], label="Temperature (°C)", color='red')
altitude_barometric_line, = ax_altitude.plot([], [], label="Barometric Altitude (m)", color='blue')
altitude_gps_line, = ax_altitude.plot([], [], label="GPS Altitude (m)", color='red')
velocity_line, = ax_velocity.plot([], [], label="Velocity (m/s)", color='green')
acceleration_line, = ax_acceleration.plot([], [], label="Acceleration Magnitude (m/s²)", color='purple')
vertical_speed_line, = ax_vertical_speed.plot([], [], label="Vertical Speed (m/s)", color='orange')
pitch_line, = ax_orientation.plot([], [], label="Pitch (°)", color='blue')
roll_line, = ax_orientation.plot([], [], label="Roll (°)", color='red')
yaw_line, = ax_orientation.plot([], [], label="Yaw (°)", color='green')
rotation_rate_line, = ax_rotation_rate.plot([], [], label="Rotation Rate (°/s)", color='magenta')
rocket_drift_line, = ax_drift.plot([], [], label="Rocket Drift (m)", color='brown')

# Set legends
for ax in axs.flatten():
    ax.legend()

# **Set Fixed Y-Axis Limits**
ax_temperature.set_ylim(0, 50)
ax_altitude.set_ylim(0, 250)
ax_velocity.set_ylim(-40, 180)
ax_acceleration.set_ylim(-60, 100)
ax_vertical_speed.set_ylim(-40, 180)
ax_orientation.set_ylim(-180, 180)
ax_rotation_rate.set_ylim(0, 20)
ax_drift.set_ylim(0, 500)

# Function to update the plot
def update_plot(frame):
    global prev_altitude, initial_latitude, initial_longitude, initial_roll

    try:
        data, addr = sock.recvfrom(1024)
        data_str = data.decode("utf-8")
        print(f"🔹 Received raw data: {data_str}")

        data_list = data_str.split(",")

        if len(data_list) >= 15:
            timestamp = data_list[0]
            temperature = float(data_list[1])
            altitude_barometric = float(data_list[2])
            altitude_gps = float(data_list[3])
            accel_x = float(data_list[4])
            accel_y = float(data_list[5])
            accel_z = float(data_list[6])
            gyro_x = float(data_list[7])
            gyro_y = float(data_list[8])
            gyro_z = float(data_list[9])
            latitude = float(data_list[13])
            longitude = float(data_list[14])

            print(f"✅ Temperature: {temperature}°C, Altitude (Baro): {altitude_barometric}m, GPS Alt: {altitude_gps}m")
            print(f"✅ Accel: X={accel_x}, Y={accel_y}, Z={accel_z}")
            print(f"✅ Gyro: X={gyro_x}, Y={gyro_y}, Z={gyro_z}")
            print(f"✅ GPS: Latitude={latitude}, Longitude={longitude}")

            # Append time dynamically
            if not time_data:
                time_data.append(0)
            else:
                time_data.append(time_data[-1] + 1)

            # Append values
            temperature_data.append(temperature)
            altitude_barometric_data.append(altitude_barometric)
            altitude_gps_data.append(altitude_gps)
            latitude_data.append(latitude)
            longitude_data.append(longitude)

            # Compute Velocity (dh/dt)
            if prev_altitude is not None:
                dt = 1  
                velocity = (altitude_barometric - prev_altitude) / dt
            else:
                velocity = 0
            velocity_data.append(velocity)
            vertical_speed_data.append(velocity)
            prev_altitude = altitude_barometric

            # Compute Acceleration Magnitude
            acceleration_magnitude = sqrt(accel_x**2 + accel_y**2 + accel_z**2)
            acceleration_magnitude_data.append(acceleration_magnitude)

            # Compute Rotation Rate Magnitude
            rotation_rate_magnitude = sqrt(gyro_x**2 + gyro_y**2 + gyro_z**2)
            rotation_rate_data.append(rotation_rate_magnitude)

            # **Fix Pitch & Roll Based on IMU Orientation**
            pitch = degrees(atan2(accel_y, sqrt(accel_x**2 + accel_z**2)))  
            roll = degrees(atan2(accel_x, sqrt(accel_y**2 + accel_z**2)))   

            # **Calibrate the roll so it starts at zero**
            if initial_roll is None:
                initial_roll = roll  # Store the first roll value

            roll -= initial_roll  # Subtract the initial offset

            yaw = degrees(atan2(accel_z, sqrt(accel_x**2 + accel_y**2)))

            orientation_pitch_data.append(pitch)
            orientation_roll_data.append(roll)
            orientation_yaw_data.append(yaw)

            # Compute Rocket Drift (Distance from Launch Site)
            if initial_latitude is None:
                initial_latitude = latitude
                initial_longitude = longitude
            drift = sqrt((latitude - initial_latitude)**2 + (longitude - initial_longitude)**2) * 111139  
            drift_data.append(drift)

            # Update plots
            temperature_line.set_data(time_data, temperature_data)
            altitude_barometric_line.set_data(time_data, altitude_barometric_data)
            altitude_gps_line.set_data(time_data, altitude_gps_data)
            velocity_line.set_data(time_data, velocity_data)
            acceleration_line.set_data(time_data, acceleration_magnitude_data)
            vertical_speed_line.set_data(time_data, vertical_speed_data)
            pitch_line.set_data(time_data, orientation_pitch_data)
            roll_line.set_data(time_data, orientation_roll_data)
            yaw_line.set_data(time_data, orientation_yaw_data)
            rocket_drift_line.set_data(time_data, drift_data)
            rotation_rate_line.set_data(time_data, rotation_rate_data)

            # Update only x-axis dynamically
            for ax in axs.flatten():
                ax.set_xlim(max(0, time_data[-1] - 100), time_data[-1] + 10)

            plt.draw()
            plt.pause(0.01)

    except socket.timeout:
        print("❌ No data received within timeout.")

ani = animation.FuncAnimation(fig, update_plot, interval=1000, blit=False, cache_frame_data=False)

plt.tight_layout()
plt.show()
