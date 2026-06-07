import serial
import time
import threading


# Configuration
PORT = "COM10"        # Windows example. On Linux, use something like "/dev/pts/3".  
BAUD_RATE = 115200
READ_TIMEOUT = 0.1

BOTTLE_INTERVAL_SEC = 4.0  
MAIN_LOOP_DELAY_SEC = 0.1


# Runtime state
system_running = threading.Event()
waiting_camera_result = threading.Event()
shutdown_event = threading.Event()

processed_count = 0



# Serial setup
try:
    arduino_sim = serial.Serial(PORT, BAUD_RATE, timeout=READ_TIMEOUT)
    print(f"Mock Arduino listening on {PORT} @ {BAUD_RATE} baud")
except Exception as error:
    print(f"Failed to open port {PORT}: {error}")
    raise SystemExit(1)



# Conveyor simulation
def simulate_conveyor() -> None:
    """Simulate bottles arriving at the camera inspection station."""
    global processed_count

    while not shutdown_event.is_set():
        if system_running.is_set() and not waiting_camera_result.is_set():
            print("\n[System] Conveyor running...")
            print(f"[Conveyor] Waiting {BOTTLE_INTERVAL_SEC:.1f}s for next bottle...")
            time.sleep(BOTTLE_INTERVAL_SEC)

            if shutdown_event.is_set():
                break

            if system_running.is_set() and not waiting_camera_result.is_set():
                processed_count += 1
                print(f"\n[Bottle #{processed_count}] Arrived at camera inspection station")
                print("[Arduino -> Dashboard] Sending CONTROL request")
                arduino_sim.write(b"CONTROL\n")
                waiting_camera_result.set()
        else:
            time.sleep(0.5)


# Main thread
def main() -> None:
    conveyor_thread = threading.Thread(target=simulate_conveyor, daemon=True)
    conveyor_thread.start()

    print("Mock Arduino started")
    print("Waiting for commands from FlexiLine dashboard...\n")
    print("Expected commands from dashboard:")
    print("   START  -> start system")
    print("   STOP   -> stop system")
    print("   B/R/N  -> camera result\n")

    try:
        while not shutdown_event.is_set():
            if arduino_sim.in_waiting > 0:
                command = arduino_sim.readline().decode("utf-8", errors="ignore").strip()

                if not command:
                    continue

                print(f"[Dashboard -> Arduino] {command}")

                if command == "START":
                    system_running.set()
                    waiting_camera_result.clear()
                    print("[Motors] Main conveyor started")
                    print("[Status] System is now RUNNING")

                elif command == "STOP":
                    system_running.clear()
                    waiting_camera_result.clear()
                    print("[Motors] System stopped")
                    print("[Status] Conveyor halted")

                elif command == "B":
                    waiting_camera_result.clear()
                    print("[Inspection] Camera result = BLUE")
                    print("[Sorting] Routing bottle to BLUE output")

                elif command == "R":
                    waiting_camera_result.clear()
                    print("[Inspection] Camera result = RED")
                    print("[Sorting] Routing bottle to RED output")

                elif command == "N":
                    waiting_camera_result.clear()
                    print("[Inspection] Camera result = NONE / INVALID")
                    print("[Sorting] Routing bottle to FINAL REJECT path")

                else:
                    print(f"[Warning] Unknown command received: {command}")

            time.sleep(MAIN_LOOP_DELAY_SEC)

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received. Shutting down mock Arduino...")

    finally:
        shutdown_event.set()
        if arduino_sim.is_open:
            arduino_sim.close()
        print("Mock Arduino stopped")


if __name__ == "__main__":
    main()