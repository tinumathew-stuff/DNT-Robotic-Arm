# Vision-Controlled 5-DOF Robotic Arm

[![Python](https://img.shields.io/badge/Language-Python_3.8+-green.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/Vision-OpenCV_4.x-red.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/AI-Google_MediaPipe_Hands-blue.svg)](https://developers.google.com/mediapipe)
[![pyFirmata](https://img.shields.io/badge/Firmware-Arduino_StandardFirmata-orange.svg)](https://github.com/tino/pyFirmata)

A computer vision-driven, gesture-controlled 5-Degree-of-Freedom (5-DOF) robotic arm. Uses real-time 3D hand landmark tracking via Google MediaPipe and OpenCV combined with trigonometric inverse kinematics (Law of Cosines) and 3D plane angles to mirror human hand gestures through an Arduino-controlled servo system in real time.

---

## Table of Contents
- [System Architecture](#system-architecture)
- [Hardware & Servo Pin Mapping](#hardware--servo-pin-mapping)
- [Kinematics & Gesture Mapping](#kinematics--gesture-mapping)
- [Features](#features)
- [Prerequisites & Dependencies](#prerequisites--dependencies)
- [Wiring & Arduino Setup](#wiring--arduino-setup)
- [Running the Project](#running-the-project)
- [Directory Structure](#directory-structure)

---

## System Architecture

```
 [ Webcam Feed ]
        │
        ▼
 [ OpenCV Frame Capture (BGR -> RGB) ]
        │
        ▼
 [ MediaPipe Hands (21 3D Landmarks) ]
        │
   ┌────┴───────────────────────────────┐
   ▼                                    ▼
[ Euclidean Distance & Gripper ]     [ 3D Plane Normal & IK ]
 - Thumb (4) to Index (8)             - Law of Cosines (A, B, C)
 - Gripper aperture mapped to Pin 5   - Plane vectors for tilt (Pin 3)
                                      - Base rotation from cx (Pin 11)
                                      - Elevation angles (Pins 9 & 10)
   └────┬───────────────────────────────┘
        ▼
 [ Motion Step-Limiter & Smoothing (`motion()`) ]
        │
        ▼
 [ pyFirmata Serial Protocol (USB COM /dev/ttyACM*) ]
        │
        ▼
 [ Arduino StandardFirmata -> 5x PWM Servos ]
```

---

## Hardware & Servo Pin Mapping

| Joint / Actuator | Servo Pin (Arduino) | Function | Gesture Source | Range |
|:---|:---:|:---|:---|:---:|
| **Base Swivel** | `Pin 11` | Pan / Azimuth rotation | Horizontal hand displacement ($c_x$) | $0^\circ - 180^\circ$ |
| **Shoulder** | `Pin 9` | Arm reach / forward extension | Law of Cosines IK ($\alpha$) | $30^\circ - 180^\circ$ |
| **Elbow** | `Pin 10` | Arm height / elevation | Vertical hand displacement ($c_y$) + IK ($\beta$) | $90^\circ - 180^\circ$ |
| **Wrist Pitch / Tilt**| `Pin 3` | End-effector orientation | 3D Hand Plane Normal Angle | $0^\circ - 180^\circ$ |
| **Gripper / Claw** | `Pin 5` | Pinch open / close | Distance between Thumb (4) & Index (8) | $30^\circ - 130^\circ$ |

---

## Kinematics & Gesture Mapping

### 1. Law of Cosines Inverse Kinematics
For linkage lengths $A = 50\text{ mm}$ and $B = 50\text{ mm}$, with target reach distance $C = \text{dist}(P_{\text{wrist}}, P_{\text{index\_mcp}})$, the joint angles are determined via:

$$\cos(\alpha) = \frac{B^2 + C^2 - A^2}{2BC}, \quad \cos(\beta) = \frac{A^2 + C^2 - B^2}{2AC}, \quad \cos(\gamma) = \frac{A^2 + B^2 - C^2}{2AB}$$

### 2. 3D Hand Plane Orientation
Vectors across wrist ($P_1$), index base ($P_5$), and pinky base ($P_{17}$) form plane vectors:

$$\vec{u} = P_5 - P_1, \quad \vec{v} = P_{17} - P_1$$
$$\vec{n} = \vec{u} \times \vec{v} = \begin{bmatrix} a \\ b \\ c \end{bmatrix}$$

The angle between normal $\vec{n}$ and the camera projection axis provides wrist tilt orientation.

### 3. Motion Smoothing
The `motion(servopin, current_pos, target_pos)` routine caps per-iteration angle deviations to $\le 5^\circ$ to prevent rapid jerks, reduce current spikes, and protect servo gearbox teeth.

---

## Features
- **Real-Time 3D Hand Tracking:** 30+ FPS landmark tracking using lightweight MediaPipe pipeline.
- **Natural Intuitive Control:** Opening your fingers opens the robotic claw; pinching fingers closes it.
- **Automated Boot Homing Sequence:** Runs a multi-stage startup test to align and exercise each joint across operating limits before enabling live tracking.
- **Fail-Safe Exception Handling:** Protects against momentary landmark occlusion without losing arm state.

---

## Prerequisites & Dependencies

### Hardware
- Arduino Uno / Nano / Mega
- 5-DOF Robotic Arm chassis with 5 servo motors (e.g., SG90 / MG996R)
- External 5V/6V 3A+ DC power supply for servos (shared ground with Arduino)
- Standard USB webcam

### Python Libraries
Install requirements:
```bash
pip install opencv-python mediapipe pyfirmata
```

---

## Wiring & Arduino Setup

1. Connect Arduino via USB to your PC.
2. In the **Arduino IDE**:
   - Go to `File -> Examples -> Firmata -> StandardFirmata`.
   - Select your board and COM port, then click **Upload**.
3. Wire the servo signal pins to Arduino pins `3`, `5`, `9`, `10`, and `11`.
4. Ensure the servo power ($V_{CC}$) and Ground ($GND$) are connected to the external 5V supply, with the external power ground bridged to Arduino $GND$.

---

## Running the Project

1. Verify and set the serial port in [`code.py`](code.py):
   ```python
   # For Linux: '/dev/ttyACM0' or '/dev/ttyUSB0'
   # For Windows: 'COM7' (or current port)
   port = '/dev/ttyACM0'
   board = Arduino(port)
   ```

2. Run the application:
   ```bash
   python3 code.py
   ```

3. Position your hand in view of the webcam. Press `q` or `Ctrl+C` to safely exit.

---

## Directory Structure

```text
DNT-Robotic-Arm/
├── angles.jpg   # Kinematic diagram showing joint angles & link lengths
├── code.py      # Real-time MediaPipe tracking, IK, and pyFirmata control
└── README.md    # System documentation
```
