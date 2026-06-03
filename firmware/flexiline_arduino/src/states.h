#pragma once

enum class SystemState {
    WAITING_START,
    START_CONVEYOR,
    BOTTLE_DETECTION,
    EVALUATE_COLOR,
    OUTPUT_CONTROL,
    FILLING_ROUTING,
    FILL_BLUE,
    FILL_RED,
    QUALITY_CONTROL,
    QUALITY_ACCEPTED,
    QUALITY_REJECTED
};

enum class DetectedColor {
    NONE,
    RED,
    BLUE,
    GREEN,
    YELLOW
};

enum class SerialCommand {
    NONE,
    START,
    STOP,
    CAMERA_BLUE,
    CAMERA_RED,
    CAMERA_NONE
};

enum class MotorDirection {
    FORWARD,
    REVERSE
};