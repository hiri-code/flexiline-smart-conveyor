#include "servos.h"

#include <Servo.h>

#include "config.h"

namespace {
    Servo mainGateServo;
    Servo fillingGateServo;
    Servo primaryRejectGateServo;
    Servo finalRejectGateServo;
}

void setupServos() {
    mainGateServo.attach(Config::MAIN_GATE_SERVO_PIN);
    fillingGateServo.attach(Config::FILLING_GATE_SERVO_PIN);
    primaryRejectGateServo.attach(Config::PRIMARY_REJECT_GATE_SERVO_PIN);
    finalRejectGateServo.attach(Config::FINAL_REJECT_GATE_SERVO_PIN);

    resetServoPositions();
}

void resetServoPositions() {
    closeMainGate();
    closeFillingGate();
    closePrimaryRejectGate();
    closeFinalRejectGate();
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

void openPrimaryRejectGate() {
    primaryRejectGateServo.write(Config::PRIMARY_REJECT_GATE_OPEN_ANGLE);
}

void closePrimaryRejectGate() {
    primaryRejectGateServo.write(Config::PRIMARY_REJECT_GATE_CLOSED_ANGLE);
}

void openFinalRejectGate() {
    finalRejectGateServo.write(Config::FINAL_REJECT_GATE_OPEN_ANGLE);
}

void closeFinalRejectGate() {
    finalRejectGateServo.write(Config::FINAL_REJECT_GATE_CLOSED_ANGLE);
}