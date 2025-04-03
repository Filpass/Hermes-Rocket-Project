import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import sqrt, atan2, degrees

# Load the CSV
df = pd.read_csv("/Users/filpas/Downloads/csv.csv")  # <--- Change this path to your CSV file

# Simulated time (1Hz)
df["Time"] = range(len(df))

# Initial calibration values
initial_total_acc = sqrt(df["Accel_X (m/s²)"][0]**2 + df["Accel_Y (m/s²)"][0]**2 + df["Accel_Z (m/s²)"][0]**2)
initial_vertical_acc = df["Accel_Z (m/s²)"][0]
initial_roll = degrees(atan2(df["Accel_X (m/s²)"][0], sqrt(df["Accel_Y (m/s²)"][0]**2 + df["Accel_Z (m/s²)"][0]**2)))

# Derived telemetry values
df["Total_Acceleration"] = df[["Accel_X (m/s²)", "Accel_Y (m/s²)", "Accel_Z (m/s²)"]].apply(
    lambda row: sqrt(row.iloc[0]**2 + row.iloc[1]**2 + row.iloc[2]**2), axis=1) - initial_total_acc
df["Vertical_Acceleration"] = df["Accel_Z (m/s²)"] - initial_vertical_acc
df["Vertical_Velocity"] = df["Altitude (m)"].diff().fillna(0)
df["Pitch"] = df[["Accel_X (m/s²)", "Accel_Y (m/s²)", "Accel_Z (m/s²)"]].apply(
    lambda row: degrees(atan2(row.iloc[1], sqrt(row.iloc[0]**2 + row.iloc[2]**2))), axis=1)
df["Roll"] = df[["Accel_X (m/s²)", "Accel_Y (m/s²)", "Accel_Z (m/s²)"]].apply(
    lambda row: degrees(atan2(row.iloc[0], sqrt(row.iloc[1]**2 + row.iloc[2]**2))), axis=1) - initial_roll
df["Yaw"] = df[["Accel_X (m/s²)", "Accel_Y (m/s²)", "Accel_Z (m/s²)"]].apply(
    lambda row: degrees(atan2(row.iloc[2], sqrt(row.iloc[0]**2 + row.iloc[1]**2))), axis=1)

# Angular rates (swapped to match live telemetry)
df["Pitch_Rate"] = df["Gyro_X (°/s)"]
df["Roll_Rate"] = df["Gyro_Y (°/s)"]
df["Yaw_Rate"] = df["Gyro_Z (°/s)"]

# Rocket drift
df["Rocket_Drift"] = df.apply(
    lambda row: sqrt((row["GPS_Latitude"] - df["GPS_Latitude"][0])**2 +
                     (row["GPS_Longitude"] - df["GPS_Longitude"][0])**2) * 111139,
    axis=1)

# Setup figure
fig, ax = plt.subplots(3, 3, figsize=(16, 12))
ax = ax.flatten()

titles = [
    "Temperature vs Time", "Altitude (Barometric & GPS) vs Time", "Vertical Velocity vs Time",
    "Total Acceleration vs Time", "Vertical Acceleration vs Time", "Orientation (Pitch, Roll, Yaw) vs Time",
    "Angular Rates (°/s) vs Time", "Rocket Drift vs Time", "GPS 2D Path"
]

ylims = [
    (0, 50), (0, 250), (-12.5, 60),
    (0, 90), (-15, 90), (-180, 180),
    (-25, 40), (0, 500), None
]

for i in range(9):
    ax[i].set_title(titles[i])
    if ylims[i]: ax[i].set_ylim(*ylims[i])
    ax[i].grid(True)

# Set GPS plot limits
lat_min, lat_max = df["GPS_Latitude"].min(), df["GPS_Latitude"].max()
lon_min, lon_max = df["GPS_Longitude"].min(), df["GPS_Longitude"].max()
if lat_min == lat_max: lat_min -= 0.0001; lat_max += 0.0001
if lon_min == lon_max: lon_min -= 0.0001; lon_max += 0.0001
ax[8].set_xlim(lat_min, lat_max)
ax[8].set_ylim(lon_min, lon_max)

# Plot lines
lines = {
    "temperature": ax[0].plot([], [], label="Temperature (°C)", color="red")[0],
    "alt_baro": ax[1].plot([], [], label="Barometric Altitude (m)", color="blue")[0],
    "alt_gps": ax[1].plot([], [], label="GPS Altitude (m)", color="red")[0],
    "velocity": ax[2].plot([], [], label="Vertical Velocity (m/s)", color="green")[0],
    "total_acc": ax[3].plot([], [], label="Total Acceleration (m/s²)", color="purple")[0],
    "vertical_acc": ax[4].plot([], [], label="Vertical Acceleration (m/s²)", color="orange")[0],
    "pitch": ax[5].plot([], [], label="Pitch (°)", color="blue")[0],
    "roll": ax[5].plot([], [], label="Roll (°)", color="red")[0],
    "yaw": ax[5].plot([], [], label="Yaw (°)", color="green")[0],
    "pitch_rate": ax[6].plot([], [], label="Pitch Rate (°/s)", color="blue")[0],
    "roll_rate": ax[6].plot([], [], label="Roll Rate (°/s)", color="red")[0],
    "yaw_rate": ax[6].plot([], [], label="Yaw Rate (°/s)", color="green")[0],
    "drift": ax[7].plot([], [], label="Rocket Drift (m)", color="brown")[0],
    "gps_path": ax[8].plot([], [], label="Path")[0],
}

for a in ax:
    a.legend()

# Update animation
def update(frame):
    t = df["Time"][:frame+1]
    lines["temperature"].set_data(t, df["Temperature (°C)"][:frame+1])
    lines["alt_baro"].set_data(t, df["Altitude (m)"][:frame+1])
    lines["alt_gps"].set_data(t, df["GPS_Altitude (m)"][:frame+1])
    lines["velocity"].set_data(t, df["Vertical_Velocity"][:frame+1])
    lines["total_acc"].set_data(t, df["Total_Acceleration"][:frame+1])
    lines["vertical_acc"].set_data(t, df["Vertical_Acceleration"][:frame+1])
    lines["pitch"].set_data(t, df["Pitch"][:frame+1])
    lines["roll"].set_data(t, df["Roll"][:frame+1])
    lines["yaw"].set_data(t, df["Yaw"][:frame+1])
    lines["pitch_rate"].set_data(t, df["Pitch_Rate"][:frame+1])
    lines["roll_rate"].set_data(t, df["Roll_Rate"][:frame+1])
    lines["yaw_rate"].set_data(t, df["Yaw_Rate"][:frame+1])
    lines["drift"].set_data(t, df["Rocket_Drift"][:frame+1])
    lines["gps_path"].set_data(df["GPS_Latitude"][:frame+1], df["GPS_Longitude"][:frame+1])
    for i in range(8):
        ax[i].set_xlim(0, max(10, t.iloc[-1]))
    return lines.values()

ani = animation.FuncAnimation(fig, update, frames=len(df), interval=1000, blit=False, repeat=False)
plt.tight_layout()
plt.show()
