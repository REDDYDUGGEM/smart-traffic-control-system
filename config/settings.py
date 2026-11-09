# config/settings.py

# Video Configuration
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
VIDEO_SOURCE = "SIMULATION"  # 0 utilizes default webcam; change to a filename like "traffic.mp4" to use a video file

# Traffic Signal Time Constraints (in seconds)
MIN_GREEN_TIME = 10
MAX_GREEN_TIME = 45
YELLOW_TIME = 3

# Hardware Mapping: Raspberry Pi GPIO Board Pins
# Maps U.S. Concurrent Phases to physical LED channels
GPIO_PIN_MAPPING = {
    "NORTH_SOUTH": {"RED": 11, "YELLOW": 12, "GREEN": 13},
    "EAST_WEST":   {"RED": 15, "YELLOW": 16, "GREEN": 18}
}