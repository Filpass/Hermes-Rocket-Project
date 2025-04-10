import time
import csv
import datetime
import adafruit_dps310
import adafruit_icm20x
import board
import busio

# Initialize I2C bus for sensors
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize DPS310 (Pressure/Altitude sensor)
dps310 = adafruit_dps310.DPS310(i2c)

# Initialize ICM-20948 (IMU sensor)
imu = adafruit_icm20x.ICM20948(i2c)

# Generate a filename with date and time
start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_filename = f"sensor_data_{start_time}.csv"

# CSV file setup
with open(csv_filename, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([
        "Timestamp", "TimeOnly", "Pressure (hPa)", "Temperature (°C)", "Altitude (m)",
        "Accel_X (m/s²)", "Accel_Y (m/s²)", "Accel_Z (m/s²)",
        "Gyro_X (°/s)", "Gyro_Y (°/s)", "Gyro_Z (°/s)",
        "Mag_X (µT)", "Mag_Y (µT)", "Mag_Z (µT)", "GPS_Latitude", "GPS_Longitude", "GPS_Altitude (m)"
    ])  # Write headers

print(f"Saving sensor data to {csv_filename}...")

try:
    while True:
        # Get current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_only = datetime.datetime.now().strftime("%H:%M:%S")  # Extract only the time part

        # Read DPS310 sensor data
        pressure = dps310.pressure  # Pressure in hPa
        temperature = dps310.temperature  # Temperature in °C
        altitude = 44330 * (1.0 - (pressure / 1023.30) ** (1.0 / 5.255))  # Altitude in meters

        # Read IMU sensor data
        accel_x, accel_y, accel_z = imu.acceleration
        gyro_x, gyro_y, gyro_z = imu.gyro
        mag_x, mag_y, mag_z = imu.magnetic

        # Dummy values for GPS (adjust if needed)
        gps_lat = 0.0
        gps_lon = 0.0
        gps_alt = 0.0

        # Append data to CSV
        with open(csv_filename, mode="a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                timestamp, time_only, pressure, temperature, altitude,
                accel_x, accel_y, accel_z,
                gyro_x, gyro_y, gyro_z,
                mag_x, mag_y, mag_z, gps_lat, gps_lon, gps_alt
            ])
            csv_file.flush()

        # Sleep for 0.1 seconds to get 10Hz rate
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n🛑 Data collection stopped by user.")
except Exception as e:
    print(f"❌ An error occurred: {e}")
