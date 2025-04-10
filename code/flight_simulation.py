import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

# Load the data (ensure the file path is correct)
file_path = '/Users/filpas/Downloads/csv.csv'
flight_data = pd.read_csv(file_path)

# Convert Timestamp to datetime format for proper plotting
flight_data['Timestamp'] = pd.to_datetime(flight_data['Timestamp'])

# Use the given Altitude directly (instead of integrating)
altitude = flight_data['Altitude (m)'].values

# Initialize arrays for pitch, roll, and yaw (assuming starting at 0)
pitch = np.zeros(len(flight_data))
roll = np.zeros(len(flight_data))
yaw = np.zeros(len(flight_data))

# Integrate gyroscope data to simulate the orientation over time
for i in range(1, len(flight_data)):
    dt = (flight_data['Timestamp'][i] - flight_data['Timestamp'][i - 1]).total_seconds()
    pitch[i] = pitch[i - 1] + flight_data['Gyro_X (°/s)'][i] * dt
    roll[i] = roll[i - 1] + flight_data['Gyro_Y (°/s)'][i] * dt
    yaw[i] = yaw[i - 1] + flight_data['Gyro_Z (°/s)'][i] * dt

# 3D Plotting setup
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Adjust axis limits for a clearer view of orientation
ax.set_xlim([-90, 90])  # Adjust roll range
ax.set_ylim([-90, 90])  # Adjust pitch range
ax.set_zlim([0, altitude.max()])  # Altitude range

# Plot trajectory in 3D space (vertical position as Z, pitch, roll as X, Y)
def update_plot(frame):
    ax.clear()
    ax.set_title("Rocket Movement Simulation")
    ax.set_xlabel("Roll (°)")
    ax.set_ylabel("Pitch (°)")
    ax.set_zlabel("Altitude (m)")

    # Plot the rocket's body (a line representing the rocket's path)
    ax.plot(roll[:frame], pitch[:frame], altitude[:frame], label="Rocket Path", color='b')
    
    # Plot the current position of the rocket with its orientation
    ax.scatter(roll[frame], pitch[frame], altitude[frame], c='r', marker='o')

    # Optionally, add the rocket's body representation (as a line)
    ax.plot([roll[frame-1], roll[frame]], [pitch[frame-1], pitch[frame]], [altitude[frame-1], altitude[frame]], color='k')

    # Show orientation over time
    ax.text(roll[frame], pitch[frame], altitude[frame], f'{frame}', color='black')

    # Add gridlines for better visibility
    ax.grid(True)

# Create animation with slower speed (increased interval)
ani = FuncAnimation(fig, update_plot, frames=len(flight_data), interval=500, repeat=False)

plt.show()
