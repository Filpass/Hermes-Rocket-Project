import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import sqrt, atan2, degrees

# Load the CSV
df = pd.read_csv("/Users/filpas/Downloads/csv.csv") %change with your directory

# Simulated time (1Hz)
df["Time"] = range(len(df))

# Derived telemetry
df["Velocity"] = df[["Accel_X (m/s²)", "Accel_Y (m/s²)", "Accel_Z (m/s²)"]].apply(
    lambda row: sqrt(row.iloc[0]**2 + row.iloc[1]**2 + row.iloc[2]**2), axis=1)
df["Vertical_Speed"] = df["Altitude (m)"].diff().fillna(0)
df["Accel_Mag"] = df["Velocity"]
df["Pitch"] = df[["Accel_X (m/s²)", "Accel_Y (m/s²)", "Accel_Z (m/s²)"]].apply(
    lambda row: degrees(atan2(row.iloc[1], sqrt(row.iloc[0]**2 + row.iloc[2]**2))), axis=1)
df["Roll"] = df[["Accel_X (m/s²)", "Accel_Y (m/s²)", "Accel_Z (m/s²)"]].apply(
    lambda row: degrees(atan2(row.iloc[0], sqrt(row.iloc[1]**2 + row.iloc[2]**2))), axis=1)
df["Yaw"] = df[["Accel_X (m/s²)", "Accel_Y (m/s²)", "Accel_Z (m/s²)"]].apply(
    lambda row: degrees(atan2(row.iloc[2], sqrt(row.iloc[0]**2 + row.iloc[1]**2))), axis=1)
df["Rotation_Rate"] = df[["Gyro_X (°/s)", "Gyro_Y (°/s)", "Gyro_Z (°/s)"]].apply(
    lambda row: sqrt(row.iloc[0]**2 + row.iloc[1]**2 + row.iloc[2]**2), axis=1)

# Setup subplots
fig, ax = plt.subplots(3, 3, figsize=(16, 12))
ax = ax.flatten()

titles = [
    "Temperature vs Time", "Altitude (Barometric & GPS) vs Time", "Velocity vs Time",
    "Acceleration Magnitude vs Time", "Vertical Speed vs Time", "Orientation (Pitch, Roll, Yaw) vs Time",
    "Rotation Rate vs Time", "Rocket Drift vs Time", "GPS 2D Path"
]
ylims = [
    (0, 50), (0, 250), (-40, 180),
    (-60, 180), (-40, 180), (-180, 180),
    (0, 20), (0, 500), None
]

for i in range(9):
    ax[i].set_title(titles[i])
    if ylims[i]: ax[i].set_ylim(*ylims[i])
    ax[i].grid(True)

# GPS plot limits
lat_min, lat_max = df["GPS_Latitude"].min(), df["GPS_Latitude"].max()
lon_min, lon_max = df["GPS_Longitude"].min(), df["GPS_Longitude"].max()
if lat_min == lat_max: lat_min -= 0.0001; lat_max += 0.0001
if lon_min == lon_max: lon_min -= 0.0001; lon_max += 0.0001
ax[8].set_xlim(lat_min, lat_max)
ax[8].set_ylim(lon_min, lon_max)

# Initialize lines with styled colors
lines = {
    "temperature": ax[0].plot([], [], label="Temperature (°C)", color="red")[0],
    "alt_baro": ax[1].plot([], [], label="Barometric Altitude (m)", color="blue")[0],
    "alt_gps": ax[1].plot([], [], label="GPS Altitude (m)", color="red")[0],
    "velocity": ax[2].plot([], [], label="Velocity (m/s)", color="green")[0],
    "v_speed": ax[4].plot([], [], label="Vertical Speed (m/s)", color="orange")[0],
    "acc_mag": ax[3].plot([], [], label="Acceleration Magnitude (m/s²)", color="purple")[0],
    "pitch": ax[5].plot([], [], label="Pitch (°)", color="blue")[0],
    "roll": ax[5].plot([], [], label="Roll (°)", color="red")[0],
    "yaw": ax[5].plot([], [], label="Yaw (°)", color="green")[0],
    "rot_rate": ax[6].plot([], [], label="Rotation Rate (°/s)", color="magenta")[0],
    "drift": ax[7].plot([], [], label="Rocket Drift (m)", color="brown")[0],
    "gps_path": ax[8].plot([], [], label="Path")[0],
}

for axis in ax:
    axis.legend()

# Update animation
def update(frame):
    t = df["Time"][:frame+1]

    lines["temperature"].set_data(t, df["Temperature (°C)"][:frame+1])
    lines["alt_baro"].set_data(t, df["Altitude (m)"][:frame+1])
    lines["alt_gps"].set_data(t, df["GPS_Altitude (m)"][:frame+1])
    lines["velocity"].set_data(t, df["Velocity"][:frame+1])
    lines["v_speed"].set_data(t, df["Vertical_Speed"][:frame+1])
    lines["acc_mag"].set_data(t, df["Accel_Mag"][:frame+1])
    lines["pitch"].set_data(t, df["Pitch"][:frame+1])
    lines["roll"].set_data(t, df["Roll"][:frame+1])
    lines["yaw"].set_data(t, df["Yaw"][:frame+1])
    lines["rot_rate"].set_data(t, df["Rotation_Rate"][:frame+1])
    lines["drift"].set_data(t, df["Altitude (m)"][:frame+1])
    lines["gps_path"].set_data(df["GPS_Latitude"][:frame+1], df["GPS_Longitude"][:frame+1])

    for i in range(8):
        ax[i].set_xlim(0, max(10, t.iloc[-1]))

    return lines.values()

ani = animation.FuncAnimation(fig, update, frames=len(df), interval=1000, blit=False, repeat=False)
plt.tight_layout()
plt.show()
