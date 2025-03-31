# Hermes Rocket Project 🚀

This repository contains all software, data, and design files used in the development and flight testing of the Hermes Rocket.

## 📂 Contents

- `Design_Fabrication_and_Testing_of_a_3D_Printed_Model_Rocket_with_Integrated_Telemetry_Systems.pdf` – Master's thesis submitted for the M.Sc. in Space Engineering at Universität Bremen
- `/cad` – 3D models of nose cone, body tube, and adapter (.STL)
- `/code` – Python scripts for telemetry collection, live plotting, and post-flight analysis
- `/data` – Raw telemetry data from each flight (CSV format)
- `/analysis` – Static plots and animations generated from telemetry

📄 [Download the full thesis (PDF)](./Design_Fabrication_and_Testing_of_a_3D_Printed_Model_Rocket_with_Integrated_Telemetry_Systems.pdf)

## 🛰️ Hardware Overview

- **Main Computer:** Raspberry Pi Zero 2W  
- **Sensors:**
  - GPS Module: PA1010D  
  - Barometric Pressure Sensor: DPS310  
  - 9-DOF IMU: ICM-20948 

## 📈 Output

Post-flight data visualization is located in the `/analysis` folder.

## 📹 Videos

Due to GitHub storage limits, flight camera and telemetry videos are hosted externally:  
🎥 [Watch on YouTube (Unlisted)](https://www.youtube.com/playlist?list=PLU9vdCkJsIVlVfhIgIDVsfnCWYGNboWbm)

## 📜 License

This project is open-source under the [MIT License](./LICENSE).
