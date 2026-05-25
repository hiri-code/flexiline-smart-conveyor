"""
FlexiLine configuration file.

This file contains the configuration settings for FlexiLine, including parameters,
system constant and configuration values.
"""

class SerialConfig:
    """Serial communication configuration for Arduino controller."""
    BAUD_RATE: int = 115200
    TIMEOUT: float = 1.0 # seconds
    RECONNECT_DELAY: float = 2.0 # seconds
    PORT_SCAN_RANGE: tuple[int, int] = (1, 33) # Range of COM ports to scan for available devices


class SerialCommands:
    """Serial protocol commands for communication with Arduino communication."""
    # Python to Arduino
    START: bytes = b"start" # Command to start the FlexiLine system
    STOP: bytes = b"stop" # Command to stop the FlexiLine system
    COLOR_BLUE: bytes = b'B' # Response code for blue color detected
    COLOR_RED: bytes = b'R' # Response code for red color detected
    COLOR_NONE: bytes = b'N' # Response code for no color detected

    # Arduino to Python
    CONTROL_REQUEST: str = "CONTROL" # Signal from Arduino requesting color detection


class CameraConfig:
    CAMERA_INDEX: int = 0 # Default camera index (0 for built-in webcam)
    FRAME_WIDTH: int = 640 
    FRAME_HEIGHT: int = 480
    MIN_COLOR_PIXELS: int = 1000 # Minimum number of pixels to confirm color detection
    
    # HSV color ranges for color detection
    # Blue color range in HSV
    LOWER_BLUE: tuple[int, int, int] = (100, 150, 0)
    UPPER_BLUE: tuple[int, int, int] = (140, 255, 255)

    # Red color range in HSV
    LOWER_RED_1: tuple[int, int, int] = (0, 120, 70)
    UPPER_RED_1: tuple[int, int, int] = (10, 255, 255)
    LOWER_RED_2: tuple[int, int, int] = (170, 120, 70)
    UPPER_RED_2: tuple[int, int, int] = (180, 255, 255)

class UIConfig:
    WINDOW_TITLE: str = "FlexiLine | Operator"
    CAMERA_LABEL_WIDTH: int = 620
    CAMERA_LABEL_HEIGHT: int = 460
    MESSAGE_DURATION_MS: int = 3000 # Duration to display status messages in milliseconds
    MESSAGE_FONT_SIZE: int = 11
    COUNTER_FONT_SIZE: int = 12 # Font size for the color counters
    COUNTER_LABEL_RED: str = "Red Count: "  # Label text for red bottle counter
    COUNTER_LABEL_BLUE: str = "Blue Count: " # Label text for blue bottle counter
    BUTTON_TOGGLE_DELAY_MS: int = 1000 # Delay in milliseconds to prevent rapid toggling of start/stop button


class ChartConfig:
    """Production chart visualization configuration."""
    CHART_TITLE: str = "Processed bottles"
    X_LABEL: str = "Time (minutes)"
    Y_LABEL: str = "Count bottles"
    RED_LINE_COLOR: str = "red" # Color for red bottle production line
    BLUE_LINE_COLOR: str = "blue" # Color for blue bottle production line
    LEGEND_RED: str = "Red bottles" # Legend label for red bottle line
    LEGEND_BLUE: str = "Blue bottles" # Legend label for blue bottle line


class StatusMessages:
    """Status messages for UI display."""
    # Serial connection messages
    SERIAL_CONNECTING: str = "Connecting {}..."
    SERIAL_CONNECTED: str = "{} Connection established"
    SERIAL_DISCONNECTING: str = "Disconnecting {}..."
    SERIAL_DISCONNECTED: str = "{} Disconnected"
    SERIAL_ERROR: str = "Serial error: {}"
    SERIAL_CLOSED: str = "Serial connection closed"
    SERIAL_READ_ERROR: str = "Error reading from serial: {}"
    SERIAL_UNEXPECTED_ERROR: str = "Unexpected serial error: {}"

    # Camera messages
    CAMERA_INITIALIZING: str = "Initializing camera..."
    CAMERA_ERROR_OPEN: str = "Error opening camera"
    CAMERA_ERROR_CAPTURE: str = "Error capturing frame from camera"
    CAMERA_ERROR_RETRY: str = "Camera error. Push 'Retry' button."
    CAMERA_RECONNECTING: str = "Reconnecting camera..."

    # Color detection messages
    COLOR_BLUE_DETECTED: str = "Blue bottle detected"
    COLOR_RED_DETECTED: str = "Red bottle detected"
    COLOR_NONE_DETECTED: str = "No registered color detected"

    # System status messages
    SYSTEM_STARTED: str = "System started"
    SYSTEM_STOPPED: str = "System stopped"

    # Close confirmation messages
    CLOSE_CONFIRMATION_TITLE: str = "Confirm Exit"
    CLOSE_CONFIRMATION_MESSAGE: str = "Are you sure you want to exit?"
    CLOSE_CONFIRMATION_YES: str = "Yes"
    CLOSE_CONFIRMATION_NO: str = "No"


class MessageColors:
    """Colors for status messages."""
    WHITE: str = "white" # Default color for status messages
    GREEN: str = "green" # Color for success messages (e.g., color detected)
    RED: str = "red" # Color for error messages (e.g., camera error)
    YELLOW: str = "yellow" # Color for warning messages (e.g., no color detected)


class ThreadConfig:
    """Threading and async operation configuration."""
    MESSAGE_CLEAR_DELAY: float = 3.0 # Seconds to wait before clearing status messages from the UI