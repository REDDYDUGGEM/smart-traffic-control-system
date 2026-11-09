# Edge AI Density-Based Smart Traffic Control System

[![Python 3.11](https://shields.io)](https://python.org)
[![YOLOv8](https://shields.io)](https://github.com)
[![Platform](https://shields.io)]()
[![License: MIT](https://shields.io)](https://opensource.org)

An end-to-end, modular optimization platform designed to mitigate urban gridlock using edge computing and real-time deep learning. The system replaces obsolete, fixed-interval traffic loops with an adaptive, data-driven cycle that modifies and optimizes green light durations based on live lane vehicle accumulation arrays.

---

## 🚀 System Architecture

This project features a decoupled, production-grade micro-architecture designed with a strict separation of concerns. Configuration metadata, machine learning pipelines, mathematical scheduling logic, and physical electronic layers are isolated into discrete Python modules:

```text
my-smart-traffic-system/
│
├── config/
│   └── settings.py          # Centralized configuration mapping (GPIO pins, thresholds)
│
├── src/
│   ├── __init__.py
│   ├── detector.py          # Vision ingestion layer & spatial YOLOv8 coordinate filter
│   ├── scheduler.py         # Optimization engine computing bounded time allocations
│   └── hardware.py          # Cross-platform GPIO abstracter with safe simulation fallback
│
├── main.py                  # Central system orchestrator and operational state machine
└── README.md
```

---

## 🧠 Key Core Modules Breakdown

### 1. Computer Vision & Spatial Coordinate Ingestion (`detector.py`)
Abstracts real-time image processing utilizing an edge-optimized **YOLOv8-Nano Neural Network**. The module tracks multi-class vehicle profiles (cars, trucks, buses, motorcycles) while simultaneously implementing a **Spatial Quadrant Partitioning Engine**.Detections are mapped to their explicit pixel boundary centers $(x, y)$ and evaluated against frame midpoint vectors to route vehicle arrays into standalone U.S. Phase tracks.

### 2. Bounded Proportional Scheduling Engine (`scheduler.py`)
Computes an optimal concurrent green-light matrix. The optimization script isolates the worst-case bottleneck lane within an active direction and runs a hard-clamped linear interpolation formula to output time allocations:
* **Primary Thru-Phases:** Generates a 15-second minimum safety floor ($\le$ 7 cars) and a 30-second maximum ceiling ($\ge$ 14 cars), fluctuating linearly inside intermediate congestion steps.
* **Protected Left-Turn Extensions:** Tracks separate left-turn pockets to scale a green arrow arrow phase dynamically between 5 and 15 seconds.

### 3. Dynamic Sensor-Driven Phase Omission Logic (`main.py`)
To prevent intersection throughput degradation, the orchestrator features built-in **Omission Logic**. If a left-turn quadrant tracking array returns exactly `0` vehicles, the system automatically suppresses that specific protected green-arrow sub-phase entirely—transitioning directly to the next lane sequence to eliminate unnecessary idling delays.

### 4. Cross-Platform Hardware Abstraction Layer (`hardware.py`)
Leverages a defensive programming structure wrapped in `try/except` handles. When deployed on physical **Raspberry Pi** chips, it maps software states directly to physical circuit relays via `RPi.GPIO`. When executed on standard desktop platforms (Windows/macOS), it catches missing hardware exceptions and smoothly drops into **Virtual Simulation Mode**, channeling diagnostic pipelines cleanly to standard logs without crashing.

---

## 💻 Installation & Quick Start

### 1. Clone the repository and navigate into the root directory:
```bash
git clone https://github.com
cd smart-traffic-control-system
```

### 2. Install dependencies:
```bash
pip install opencv-python ultralytics
```

### 3. Run the orchestration loop:
```bash
python main.py
```

*Note: By default, if an external video source asset is missing, the codebase automatically boots into **Virtual Simulation Mode**, generating dynamic traffic pattern metrics across your console.*

---

## 🛠️ Technical Competencies Demonstrated
* **Languages & Architecture:** Python (Object-Oriented Programming, Solid Design Principles)
* **Deep Learning Frameworks:** YOLOv8 (Inference Batch Handling, Class Threshold Filtering)
* **Computer Vision:** OpenCV (Video Ingestion, Frame Dimensional Scaling)
* **Embedded System Patterns:** Hardware Abstraction Layers (HAL), Cross-Platform Fail-safes, GPIO Interface Mapping
