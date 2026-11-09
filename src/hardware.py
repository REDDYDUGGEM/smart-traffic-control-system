# src/hardware.py
import sys
from config.settings import GPIO_PIN_MAPPING

# Gracefully intercept ImportError if executing on standard development PCs without GPIO headers
try:
    import RPi.GPIO as GPIO
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class HardwareController:
    """
    Directly interfaces with physical circuits or routes status data to console logs.
    """
    def __init__(self):
        if HAS_HARDWARE:
            GPIO.setmode(GPIO.BOARD)
            # Initialize all target signal channels as low-voltage active outputs
            for lane, lights in GPIO_PIN_MAPPING.items():
                for light_color, pin in lights.items():
                    GPIO.setup(pin, GPIO.OUT)
                    GPIO.output(pin, GPIO.LOW)
        else:
            print("[SYSTEM NOTICE] Hardware abstractions loaded in Virtual Simulation Mode.")

    def set_signal_state(self, active_lane, state):
        """
        Manipulates physical pins or streams state machine events cleanly to terminal outputs.
        State choices: 'GREEN', 'YELLOW', 'RED'
        """
        if HAS_HARDWARE:
            # High-fidelity electrical logic goes here (e.g., matching pin outputs to state variables)
            pass
        else:
            print(f" -> [HARDWARE SIMULATION] Lane: {active_lane} updated to state: {state}")
            
    def cleanup(self):
        if HAS_HARDWARE:
            GPIO.cleanup()