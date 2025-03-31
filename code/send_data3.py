import time
import csv
import socket
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

# UDP setup
UDP_IP = "192.168.1.4"  # Replace with your Mac's IP
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Reference pressure at sea level (adjust as per your location)
SEA_LEVEL_PRESSURE = 1023.30  # hPa

# Generate a filename with date and time
start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_filename = f"sensor_data_{start_time}.csv"

# CSV file setup
with open(csv_filename, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([
        "Timestamp", "Pressure (hPa)", "Temperature (°C)", "Altitude (m)",
        "Accel_X (m/s²)", "Accel_Y (m/s²)", "Accel_Z (m/s²)",
        "Gyro_X (°/s)", "Gyro_Y (°/s)", "Gyro_Z (°/s)",
        "Mag_X (µT)", "Mag_Y (µT)", "Mag_Z (µT)", "GPS_Latitude", "GPS_Longitude", "GPS_Altitude (m)"
    ])  # Write headers

print(f"Saving sensor data to {csv_filename}...")

try:
    while True:
        # Get current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Read DPS310 sensor data
        pressure = dps310.pressure  # Pressure in hPa
        temperature = dps310.temperature  # Temperature in °C
        altitude = 44330 * (1.0 - (pressure / SEA_LEVEL_PRESSURE) ** (1.0 / 5.255))  # Altitude in meters

        # Read IMU sensor data
        accel_x, accel_y, accel_z = imu.acceleration
        gyro_x, gyro_y, gyro_z = imu.gyro
        mag_x, mag_y, mag_z = imu.magnetic

        # Dummy values for GPS
        gps_lat = 0.0
        gps_lon = 0.0
        gps_alt = 0.0

        # Prepare data string for UDP transmission
        data = f"{timestamp},{temperature:.2f},{altitude:.2f},{gps_alt:.2f}," \
               f"{accel_x:.2f},{accel_y:.2f},{accel_z:.2f}," \
               f"{gyro_x:.2f},{gyro_y:.2f},{gyro_z:.2f}," \
               f"{mag_x:.2f},{mag_y:.2f},{mag_z:.2f}," \
               f"{gps_lat:.6f},{gps_lon:.6f}"

        # Send UDP packet
        try:
            sock.sendto(data.encode('utf-8'), (UDP_IP, UDP_PORT))
            print(f"🔹 Sent: {data}")
            print(f"   ✅ Pressure: {pressure:.2f} hPa")
        except Exception as e:
            print(f"⚠️ Warning: Failed to send telemetry, but data is still logged. Error: {e}")

        # Append data to CSV
        with open(csv_filename, mode="a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                timestamp, pressure, temperature, altitude,
                accel_x, accel_y, accel_z,
                gyro_x, gyro_y, gyro_z,
                mag_x, mag_y, mag_z, gps_lat, gps_lon, gps_alt
            ])
            csv_file.flush()

        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Data collection stopped by user.")
except Exception as e:
    print(f"❌ An error occurred: {e}")
