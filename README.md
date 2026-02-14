# Fruit Ninja (Computer Vision Game)

A real-time, interactive game built with **Python**, **OpenCV**, and **MediaPipe**. This project uses Computer Vision (CV) to track the player's hand movements, allowing them to slice virtual fruits on screen using their finger as a blade.

![Project Status](https://img.shields.io/badge/Status-Playable_Prototype-brightgreen) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![OpenCV](https://img.shields.io/badge/Library-OpenCV-red)


## Features
* **Hand Tracking:** Uses MediaPipe to track the index finger tip in real-time (60 FPS).
* **Physics Engine:** Custom gravity and projectile motion logic simulates realistic fruit tossing.
* **Dynamic Blade:** A fading "swoosh" trail follows the finger using a deque buffer for smooth rendering.
* **Collision Detection:** Euclidean distance calculations determine when the "blade" intersects with fruit coordinates.
* **Particle System:** Fruits explode into smaller colored particles upon slicing.
* **Multi-Directional Spawning:** Fruits spawn from all four sides of the screen with randomized velocities.

## 🛠️ Tech Stack
* **Language:** Python
* **Libraries:**
    * `opencv-python` (Image processing & drawing)
    * `mediapipe` (Hand landmark detection)
    * `numpy` (Math operations)

## How to Run Locally

### 1. Prerequisites
You need Python installed. If you are on a Mac (M1/M2), it is highly recommended to use a Conda environment to avoid version conflicts.

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/nishitawaghela/fruit_ninja_CV.git](https://github.com/nishitawaghela/fruit_ninja_CV.git)
cd fruit_ninja_CV

# (Optional but recommended) Create a virtual environment
conda create -n fruit_ninja python=3.10 -y
conda activate fruit_ninja

# Install dependencies
pip install opencv-python mediapipe