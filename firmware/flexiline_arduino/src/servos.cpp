#include "servos.h"

#include <Servo.h>

#include "config.h"

namespace {
    Servo mainGateServo;
    Servo fillingGateServo;
    Servo rejectGateServo;
}

void setupServos() {
    mainGateServo.attach(Config::MAIN_GATE_SERVO_PIN);
    fillingGateServo.attach(Config::FILLING_GATE_SERVO_PIN);
    rejectGateServo.attach(Config::REJECT_GATE_SERVO_PIN);

    resetServoPositions();
}

void resetServoPositions() {
    closeMainGate();
    closeFillingGate();
    closeRejectGate();
}

void openMainGate() {
    mainGateServo.write(Config::MAIN_GATE_OPEN_ANGLE);
}

void closeMainGate() {
    mainGateServo.write(Config::MAIN_GATE_CLOSED_ANGLE);
}

void openFillingGate() {
    fillingGateServo.write(Config::FILLING_GATE_OPEN_ANGLE);
}

void closeFillingGate() {
    fillingGateServo.write(Config::FILLING_GATE_CLOSED_ANGLE);
}

void openRejectGate() {
    rejectGateServo.write(Config::REJECT_GATE_OPEN_ANGLE);
}

void closeRejectGate() {
    rejectGateServo.write(Config::REJECT_GATE_CLOSED_ANGLE);
}