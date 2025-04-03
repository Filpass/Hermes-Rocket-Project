import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
from math import sqrt, atan2, degrees

# Set up UDP
HOST = '0.0.0.0'
PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.settimeout(2)

# Data storage
time_data = []
temperature_data = []
altitude_barometric_data = []
altitude_gps_data = []
vertical_velocity_data = []
total_acceleration_data = []
vertical_acceleration_data = []
pitch_data = []
roll_data = []
yaw_data = []
pitch_rate_data = []
roll_rate_data = []
yaw_rate_data = []
drift_data = []
latitude_data = []
longitude_data = []

# Calibration references
prev_altitude = None
initial_lat = None
initial_lon = None
initial_total_acc = None
initial_vert_acc = None
initial_roll = None

# Plot setup
fig, ax = plt.subplots(3, 3, figsize=(16, 12))
ax = ax.flatten()

titles = [
    "Temperature vs Time", "Altitude (Barometric & GPS) vs Time", "Vertical Velocity vs Time",
    "Total Acceleration vs Time", "Vertical Acceleration vs Time", "Orientation (Pitch, Roll, Yaw)",
    "Angular Rates (Pitch, Roll, Yaw)", "Rocket Drift vs Time", "GPS 2D Path"
]
ylims = [
    (0, 50), (0, 250), (-12.5, 60),
    (0, 90), (0, 90), (-180, 180),
    (-25, 40), (0, 500), None
]

for i in range(9):
    ax[i].set_title(titles[i])
    if ylims[i]: ax[i].set_ylim(*ylims[i])
    ax[i].grid(True)

# Line definitions
lines = {
    "temperature": ax[0].plot([], [], label="Temp (°C)", color='red')[0],
    "alt_baro": ax[1].plot([], [], label="Baro (m)", color='blue')[0],
    "alt_gps": ax[1].plot([], [], label="GPS (m)", color='red')[0],
    "vertical_velocity": ax[2].plot([], [], label="Vert Vel (m/s)", color='green')[0],
    "total_acc": ax[3].plot([], [], label="Total Acc (m/s²)", color='purple')[0],
    "vert_acc": ax[4].plot([], [], label="Vert Acc (m/s²)", color='orange')[0],
    "pitch": ax[5].plot([], [], label="Pitch (°)", color='blue')[0],
    "roll": ax[5].plot([], [], label="Roll (°)", color='red')[0],
    "yaw": ax[5].plot([], [], label="Yaw (°)", color='green')[0],
    "pitch_rate": ax[6].plot([], [], label="Pitch Rate (°/s)", color='blue')[0],
    "roll_rate": ax[6].plot([], [], label="Roll Rate (°/s)", color='red')[0],
    "yaw_rate": ax[6].plot([], [], label="Yaw Rate (°/s)", color='green')[0],
    "drift": ax[7].plot([], [], label="Drift (m)", color='brown')[0],
    "gps_path": ax[8].plot([], [], label="GPS Path")[0],
}

for a in ax: a.legend()

# Update function
def update_plot(frame):
    global prev_altitude, initial_lat, initial_lon
    global initial_total_acc, initial_vert_acc, initial_roll

    try:
        data, _ = sock.recvfrom(1024)
        fields = data.decode("utf-8").strip().split(",")

        if len(fields) >= 15:
            temperature = float(fields[1])
            altitude = float(fields[2])
            gps_alt = float(fields[3])
            ax_, ay_, az_ = float(fields[4]), float(fields[5]), float(fields[6])
            gx_, gy_, gz_ = float(fields[7]), float(fields[8]), float(fields[9])
            lat, lon = float(fields[13]), float(fields[14])

            # Time
            t = time_data[-1] + 1 if time_data else 0
            time_data.append(t)

            # Base telemetry
            temperature_data.append(temperature)
            altitude_barometric_data.append(altitude)
            altitude_gps_data.append(gps_alt)
            latitude_data.append(lat)
            longitude_data.append(lon)

            # Vertical Velocity
            if prev_altitude is not None:
                vertical_velocity_data.append(altitude - prev_altitude)
            else:
                vertical_velocity_data.append(0)
            prev_altitude = altitude

            # Total acceleration (calibrated)
            total_acc = sqrt(ax_**2 + ay_**2 + az_**2)
            if initial_total_acc is None:
                initial_total_acc = total_acc
            total_acceleration_data.append(total_acc - initial_total_acc)

            # Vertical acceleration
            if initial_vert_acc is None:
                initial_vert_acc = az_
            vertical_acceleration_data.append(az_ - initial_vert_acc)

            # Orientation
            pitch = degrees(atan2(ay_, sqrt(ax_**2 + az_**2)))
            roll = degrees(atan2(ax_, sqrt(ay_**2 + az_**2)))
            yaw = degrees(atan2(az_, sqrt(ax_**2 + ay_**2)))
            if initial_roll is None:
                initial_roll = roll
            roll -= initial_roll
            pitch_data.append(pitch)
            roll_data.append(roll)
            yaw_data.append(yaw)

            # Angular Rates
            pitch_rate_data.append(gx_)
            roll_rate_data.append(gy_)
            yaw_rate_data.append(gz_)

            # Rocket Drift
            if initial_lat is None:
                initial_lat = lat
                initial_lon = lon
            drift = sqrt((lat - initial_lat)**2 + (lon - initial_lon)**2) * 111139
            drift_data.append(drift)

            # Update plots
            lines["temperature"].set_data(time_data, temperature_data)
            lines["alt_baro"].set_data(time_data, altitude_barometric_data)
            lines["alt_gps"].set_data(time_data, altitude_gps_data)
            lines["vertical_velocity"].set_data(time_data, vertical_velocity_data)
            lines["total_acc"].set_data(time_data, total_acceleration_data)
            lines["vert_acc"].set_data(time_data, vertical_acceleration_data)
            lines["pitch"].set_data(time_data, pitch_data)
            lines["roll"].set_data(time_data, roll_data)
            lines["yaw"].set_data(time_data, yaw_data)
            lines["pitch_rate"].set_data(time_data, pitch_rate_data)
            lines["roll_rate"].set_data(time_data, roll_rate_data)
            lines["yaw_rate"].set_data(time_data, yaw_rate_data)
            lines["drift"].set_data(time_data, drift_data)
            lines["gps_path"].set_data(latitude_data, longitude_data)

            # X-axis limits
            for a in ax[:8]:
                a.set_xlim(max(0, t - 100), t + 10)

    except socket.timeout:
        print("No data received (timeout)")

ani = animation.FuncAnimation(fig, update_plot, interval=1000, blit=False)
plt.tight_layout()
plt.show()
