# main.py
import cv2
import time
import os
from config.settings import VIDEO_SOURCE, FRAME_WIDTH, FRAME_HEIGHT, YELLOW_TIME
from src.detector import VehicleDetector
from src.scheduler import TrafficScheduler
from src.hardware import HardwareController

def run_traffic_system():
    print("=========================================================")
    print("Starting U.S. Protected-Permissive Phase Traffic Unit")
    print("=========================================================")

    detector = VehicleDetector()
    scheduler = TrafficScheduler()
    hardware = HardwareController()

    capture = None
    has_camera = False

    # Dynamic Ingestion Evaluation: Fallback validation block
    if isinstance(VIDEO_SOURCE, int):
        # Numeric index targets local hardware webcam
        capture = cv2.VideoCapture(VIDEO_SOURCE)
        has_camera = capture.isOpened()
    elif isinstance(VIDEO_SOURCE, str):
        # Verify if the configured video filename actually exists in the workspace directory
        if os.path.exists(VIDEO_SOURCE):
            capture = cv2.VideoCapture(VIDEO_SOURCE)
            has_camera = capture.isOpened()
            if has_camera:
                print(f"[SYSTEM NOTICE] Video asset found. Ingesting track file: '{VIDEO_SOURCE}'")
        else:
            print(f"[SYSTEM WARNING] Target video track asset '{VIDEO_SOURCE}' was not found.")

    if has_camera and capture is not None:
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    else:
        print("[SYSTEM NOTICE] Running in high-fidelity autonomous simulation mode.")

    # Phase dictionary grouping straight through-lanes vs left-turn extension lanes
    phases = {
        "NORTH_SOUTH": {"THRU": ["NORTH_THRU", "SOUTH_THRU"], "LEFT": ["NORTH_LEFT", "SOUTH_LEFT"]},
        "EAST_WEST":   {"THRU": ["EAST_THRU", "WEST_THRU"],   "LEFT": ["EAST_LEFT", "WEST_LEFT"]}
    }
    
    try:
        while True:
            ret, frame = False, None
            if has_camera and capture is not None:
                ret, frame = capture.read()
                # If a local video clip hits its end loop, reset frame to trigger simulation fallback arrays
                if not ret: 
                    frame = None 
            
            density_matrix = detector.get_lane_densities(frame)
            total_vehicles = sum(density_matrix.values())
            
            print(f"\n--- Intersection Status Metric (Total Queue Load: {total_vehicles}) ---")
            print(f" N-S Lanes: Thru-Bottleneck={max(density_matrix['NORTH_THRU'], density_matrix['SOUTH_THRU'])} | Left-Bottleneck={max(density_matrix['NORTH_LEFT'], density_matrix['SOUTH_LEFT'])}")
            print(f" E-W Lanes: Thru-Bottleneck={max(density_matrix['EAST_THRU'], density_matrix['WEST_THRU'])} | Left-Bottleneck={max(density_matrix['EAST_LEFT'], density_matrix['WEST_LEFT'])}")

            for phase_name, lanes in phases.items():
                # -------------------------------------------------------------
                # STEP A: RUN PRIMARY THROUGH-TRAFFIC PHASES
                # -------------------------------------------------------------
                thru_bottleneck = max(density_matrix[l] for l in lanes["THRU"])
                allocated_green_duration = scheduler.compute_green_duration(thru_bottleneck, total_vehicles)
                
                print(f"\n[PHASE CHANGE] Activating Thru-Traffic Phase: {phase_name}")
                print(f" -> Allocation: {allocated_green_duration} seconds (Vehicles can turn left only if yielding).")
                
                hardware.set_signal_state(phase_name, "GREEN")
                time.sleep(allocated_green_duration)
                
                # -------------------------------------------------------------
                # STEP B: RUN DYNAMIC PROTECTED LEFT-TURN ARROW EXTENSIONS
                # -------------------------------------------------------------
                left_bottleneck = max(density_matrix[l] for l in lanes["LEFT"])
                
                if left_bottleneck == 0:
                    print(f" -> [LEFT-ARROW OMISSION] Left-turn pockets clear for {phase_name}. Skipping protected arrow phase.")
                else:
                    allocated_arrow_duration = scheduler.compute_left_turn_extension(left_bottleneck)
                    print(f" -> [LEFT-ARROW EXTENSION] Activating protected left arrow for {phase_name}")
                    print(f" -> Strategy: Allocating {allocated_arrow_duration} extra seconds based on {left_bottleneck} left-turning cars.")
                    
                    hardware.set_signal_state(f"{phase_name}_LEFT_ARROW", "GREEN")
                    time.sleep(allocated_arrow_duration)

                # Clear phase with standard yellow clearance
                hardware.set_signal_state(phase_name, "YELLOW")
                time.sleep(YELLOW_TIME)
                hardware.set_signal_state(phase_name, "RED")

    except KeyboardInterrupt:
        print("\nSystem execution intercepted safely by user. Initiating teardown...")
    finally:
        if has_camera and capture is not None: 
            capture.release()
        hardware.cleanup()
        cv2.destroyAllWindows()
        print("System shutdown sequence completed successfully.")

if __name__ == "__main__":
    run_traffic_system()