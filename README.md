# RPi Blind Stick: Smart Navigation Aid for Visually Impaired

## Description  
A Raspberry Pi-based assistive device designed to enhance navigation for visually impaired users. Combines ultrasonic sensors, GPS tracking, face recognition, text-to-speech (TTS), and environmental alerts to detect obstacles, identify faces, and provide real-time spatial audio feedback. Includes web integration for location sharing.

## Key Features  
- **Obstacle Detection**: 4-direction ultrasonic ranging (front/back/left/right)  
- **GPS Tracking**: Real-time latitude/longitude logging with NMEA parsing  
- **Face Recognition**: Pre-trained face database with OpenCV integration  
- **Environmental Alerts**: Water detection, light level monitoring (day/night mode)  
- **Multi-Output Feedback**: 16x2 LCD display + TTS voice announcements  
- **Safety Mechanisms**: Buzzer/motor alerts for immediate obstacles (<10 cm)  

## Hardware Components  
- Raspberry Pi (3B+/4 recommended)  
- HC-SR04 Ultrasonic Sensors (×4)  
- NEO-7M GPS Module  
- LDR Light Sensor + Water Detection Sensor  
- 5V Buzzer + Vibration Motor  
- 16x2 Character LCD  

## Pin Mapping  
| Component       | GPIO Pins            |  
|-----------------|----------------------|  
| Buzzer          | 18                   |  
| Vibration Motor | 8                    |  
| Water Sensor    | 7                    |  
| LDR Sensor      | 1                    |  
| **Front Sensor**| Echo:13, Trigger:6   |  
| **Left Sensor** | Echo:12, Trigger:16  |  
| **Right Sensor**| Echo:20, Trigger:21  |  
| **Bottom Sensor**| Echo:26, Trigger:19  |  
| LCD (I2C)       | Configured via Adafruit_CharLCD library |  

*Note: Pin assignments may require adjustment based on GPIO availability and PCB layout.*

## Project Structure  
- `gps.py`: NMEA message parser for Neo-7M GPS module  
- `FaceDetect.py`: Face recognition system using `face_recognition` library  
- `sonarTest.py`: Multi-sensor distance measurement subsystem  
- `tts.py`: Text-to-speech engine (pyttsx3) interface  
- `FinalApp.py`: Main application integrating all modules with threaded execution  

## Dependencies  
- Python Libraries: `gpiozero`, `face_recognition`, `opencv-python`, `pyttsx3`, `requests`  
- Hardware: Requires enabled serial interface (`/dev/serial0`) for GPS  
- Face Database: Stores authorized faces as JPG files in `/Faces/` directory  

![System Block Diagram](./diagram.png)  
*Schematic shown for conceptual purposes; actual connections may vary.*
