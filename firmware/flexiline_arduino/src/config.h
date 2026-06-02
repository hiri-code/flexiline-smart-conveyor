#pragma once

#include <Arduino.h>

namespace Config {
    // >>>>>>>>>>>>>>>>>>>> Serial communication <<<<<<<<<<<<<<<<<<<<

    constexpr unsigned long SERIAL_BAUD_RATE = 115200;

    // Commands received from Python
    constexpr char CMD_START[] = "START";
    constexpr char CMD_STOP[] = "STOP";
    constexpr char CMD_CAMERA_BLUE[] = "B";
    constexpr char CMD_CAMERA_RED[] = "R";
    constexpr char CMD_CAMERA_NONE[] = "N";

    // Commands sent to Python
    constexpr char CMD_CONTROL_REQUEST[] = "CONTROL";


    // >>>>>>>>>>>>>>>>>>>> Motor pins <<<<<<<<<<<<<<<<<<<<

    // Main conveyor motor
    constexpr uint8_t MAIN_CONVEYOR_PWM_PIN = 11;

    // Sorting conveyor motor
    constexpr uint8_t SORTER_CONVEYOR_RPWM_PIN = 12;
    constexpr uint8_t SORTER_CONVEYOR_LPWM_PIN = 13;


    // >>>>>>>>>>>>>>>>>>>> Pump-dispensing pins <<<<<<<<<<<<<<<<<<<<

    constexpr uint8_t BLUE_PUMP_PIN = A7;
    constexpr uint8_t RED_PUMP_PIN = A6;


    // >>>>>>>>>>>>>>>>>>>> Proximity-position sensor pins <<<<<<<<<<<<<<<<<<<<

    // Start-bottle presence sensor
    constexpr uint8_t ENTRY_SENSOR_PIN = 35;

    // Color sensor station proximity sensor
    constexpr uint8_t COLOR_STATION_SENSOR_PIN = 10;

    // Filling station sensors
    constexpr uint8_t BLUE_FILL_SENSOR_PIN = A5;
    constexpr uint8_t RED_FILL_SENSOR_PIN = 28;

    // Camera inspection station sensor
    constexpr uint8_t CAMERA_STATION_SENSOR_PIN = 8;

    // Final output sensors
    constexpr uint8_t RED_OUTPUT_SENSOR_PIN = A9;
    constexpr uint8_t BLUE_OUTPUT_SENSOR_PIN = 9;

    // Reject-waste sensors
    constexpr uint8_t REJECT_SENSOR_1_PIN = 50;
    constexpr uint8_t REJECT_SENSOR_2_PIN = 14;


    // >>>>>>>>>>>>>>>>>>>> Servo pins <<<<<<<<<<<<<<<<<<<<

    constexpr uint8_t MAIN_GATE_SERVO_PIN = 2;
    constexpr uint8_t FILLING_GATE_SERVO_PIN = 3;
    constexpr uint8_t REJECT_GATE_SERVO_PIN = 4;

    // >>>>>>>>>>>>>>>>>>>> Servo position <<<<<<<<<<<<<<<<<<<<

    // Main gate servo
    constexpr uint8_t MAIN_GATE_CLOSED_ANGLE = 180;
    constexpr uint8_t MAIN_GATE_OPEN_ANGLE = 90;

    // Filling gate servo
    constexpr uint8_t FILLING_GATE_CLOSED_ANGLE = 0;
    constexpr uint8_t FILLING_GATE_OPEN_ANGLE = 90;

    // Reject gate servo
    constexpr uint8_t REJECT_GATE_CLOSED_ANGLE = 180;
    constexpr uint8_t REJECT_GATE_OPEN_ANGLE = 105;


    // >>>>>>>>>>>>>>>>>>>> Color sensor pins <<<<<<<<<<<<<<<<<<<<

    constexpr uint8_t COLOR_SENSOR_S0_PIN = A0;
    constexpr uint8_t COLOR_SENSOR_S1_PIN = A1;
    constexpr uint8_t COLOR_SENSOR_S2_PIN = A2;
    constexpr uint8_t COLOR_SENSOR_S3_PIN = A3;
    constexpr uint8_t COLOR_SENSOR_OUT_PIN = A4;

    // Color sensor frequency scaling
    constexpr uint8_t COLOR_SENSOR_S0_STATE = LOW;
    constexpr uint8_t COLOR_SENSOR_S1_STATE = HIGH;


    // >>>>>>>>>>>>>>>>>>>> Motor configuration <<<<<<<<<<<<<<<<<<<<

    constexpr uint8_t MAIN_CONVEYOR_SPEED = 50;
    constexpr uint8_t SORTER_CONVEYOR_SPEED = 50;


    // >>>>>>>>>>>>>>>>>>>> Timing configuration <<<<<<<<<<<<<<<<<<<<

    constexpr unsigned long SERIAL_TIMEOUT_MS = 50;
    constexpr unsigned long STARTUP_DELAY_MS = 500;
    constexpr unsigned long DETECTION_COOLDOWN_MS = 1000;
    constexpr unsigned long BLUE_FILLING_TIME_MS = 5000;
    constexpr unsigned long RED_FILLING_TIME_MS = 5000;
    constexpr unsigned long CAMERA_RESPONSE_TIMEOUT_MS = 5000;
    constexpr unsigned long REJECT_DELAY_MS = 5000;


    // >>>>>>>>>>>>>>>>>>>> Color sensor configuration <<<<<<<<<<<<<<<<<<<<

    constexpr uint8_t COLOR_SENSOR_SAMPLE_COUNT = 10;
    constexpr uint16_t COLOR_DIFFERENCE_THRESHOLD = 50;
    constexpr uint16_t YELLOW_BALANCE_THRESHOLD = 30;


    // >>>>>>>>>>>>>>>>>>>> Relay logic <<<<<<<<<<<<<<<<<<<<

    // Current relay module appears to be active-low:
    // LOW  = pump ON
    // HIGH = pump OFF
    constexpr uint8_t RELAY_ON = LOW;
    constexpr uint8_t RELAY_OFF = HIGH;


    // >>>>>>>>>>>>>>>>>>>> Sensor logic <<<<<<<<<<<<<<<<<<<<

    // Sensors use INPUT_PULLUP in the original firmware.
    // LOW means detection is active.
    constexpr uint8_t SENSOR_ACTIVE = LOW;
    constexpr uint8_t SENSOR_INACTIVE = HIGH;

}