#include "motors.h"
#include "config.h"

void setupMotors() {
    pinMode(Config::MAIN_CONVEYOR_PWM_PIN, OUTPUT);
    pinMode(Config::SORTER_CONVEYOR_RPWM_PIN, OUTPUT);
    pinMode(Config::SORTER_CONVEYOR_LPWM_PIN, OUTPUT);

    stopAllMotors();
}

void startMainConveyor(uint8_t speed) {
    analogWrite(Config::MAIN_CONVEYOR_PWM_PIN, speed);
}

void stopMainConveyor() {
    analogWrite(Config::MAIN_CONVEYOR_PWM_PIN, 0);
}

void startSorterConveyor(uint8_t speed, MotorDirection direction) {
    if (direction == MotorDirection::FORWARD) {
        analogWrite(Config::SORTER_CONVEYOR_LPWM_PIN, 0);
        analogWrite(Config::SORTER_CONVEYOR_RPWM_PIN, speed);
    } else {
        analogWrite(Config::SORTER_CONVEYOR_RPWM_PIN, 0);
        analogWrite(Config::SORTER_CONVEYOR_LPWM_PIN, speed);
    }
}

void stopSorterConveyor() {
    analogWrite(Config::SORTER_CONVEYOR_RPWM_PIN, 0);
    analogWrite(Config::SORTER_CONVEYOR_LPWM_PIN, 0);
}

void stopAllMotors() {
    stopMainConveyor();
    stopSorterConveyor();
}