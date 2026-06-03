#include <Arduino.h>

#include "config.h"
#include "serial_protocol.h"
#include "states.h"
#include "motors.h"
#include "pumps.h"
#include "servos.h"
#include "color_sensor.h"

// >>>>>>>>>>>>>>>>>>>> System state <<<<<<<<<<<<<<<<<<<<

SystemState currentState = SystemState::WAITING_START;

DetectedColor physicalColor = DetectedColor::NONE;
DetectedColor cameraColor = DetectedColor::NONE;

unsigned long lastDetectionTime = 0;
unsigned long stateStartTime = 0;


// >>>>>>>>>>>>>>>>>>>> Function declarations <<<<<<<<<<<<<<<<<<<<

void setupSystem();
void resetSystem();

void runStateMachine(SerialCommand command);
void handleGlobalCommand(SerialCommand command);

void changeState(SystemState newState);
bool isSensorActive(uint8_t pin);
bool hasElapsed(unsigned long startTime, unsigned long duration);


// >>>>>>>>>>>>>>>>>>>> Arduino setup - loop <<<<<<<<<<<<<<<<<<<<

void setup() {
    Serial.begin(Config::SERIAL_BAUD_RATE);
    Serial.setTimeout(Config::SERIAL_TIMEOUT_MS);

    setupSystem();

    Serial.println("FlexiLine firmware ready");
}

void loop() {
    SerialCommand command = readSerialCommand();

    handleGlobalCommand(command);
    runStateMachine(command);
}


// >>>>>>>>>>>>>>>>>>>> System setup-reset <<<<<<<<<<<<<<<<<<<<

void setupSystem() {
    setupMotors();
    setupPumps();
    setupServos();
    setupColorSensor();

    pinMode(Config::ENTRY_SENSOR_PIN, INPUT_PULLUP);
    pinMode(Config::COLOR_STATION_SENSOR_PIN, INPUT_PULLUP);
    pinMode(Config::BLUE_FILL_SENSOR_PIN, INPUT_PULLUP);
    pinMode(Config::RED_FILL_SENSOR_PIN, INPUT_PULLUP);
    pinMode(Config::CAMERA_STATION_SENSOR_PIN, INPUT_PULLUP);
    pinMode(Config::RED_OUTPUT_SENSOR_PIN, INPUT_PULLUP);
    pinMode(Config::BLUE_OUTPUT_SENSOR_PIN, INPUT_PULLUP);
    pinMode(Config::REJECT_SENSOR_1_PIN, INPUT_PULLUP);
    pinMode(Config::REJECT_SENSOR_2_PIN, INPUT_PULLUP);

    resetSystem();
}

void resetSystem() {
    stopAllMotors();
    stopAllPumps();
    resetServoPositions();

    physicalColor = DetectedColor::NONE;
    cameraColor = DetectedColor::NONE;

    lastDetectionTime = 0;

    changeState(SystemState::WAITING_START);
}


// >>>>>>>>>>>>>>>>>>>> Global command handling <<<<<<<<<<<<<<<<<<<<

void handleGlobalCommand(SerialCommand command) {
    if (command == SerialCommand::STOP) {
        Serial.println("STOP received");
        resetSystem();
    }
}


// >>>>>>>>>>>>>>>>>>>> State machine <<<<<<<<<<<<<<<<<<<<

void runStateMachine(SerialCommand command) {
    switch (currentState) {
        case SystemState::WAITING_START:
            if (command == SerialCommand::START) {
                Serial.println("START received");
                changeState(SystemState::START_CONVEYOR);
            }
            break;

        case SystemState::START_CONVEYOR:
            Serial.println("Starting main conveyor");
            closeMainGate();
            closeFillingGate();
            closeRejectGate();
            stopSorterConveyor();
            startMainConveyor(Config::MAIN_CONVEYOR_SPEED);
            changeState(SystemState::BOTTLE_DETECTION);
            break;

        case SystemState::BOTTLE_DETECTION:
            if (
                isSensorActive(Config::COLOR_STATION_SENSOR_PIN) &&
                hasElapsed(lastDetectionTime, Config::DETECTION_COOLDOWN_MS)
            ) {
                lastDetectionTime = millis();
                stopMainConveyor();
                closeMainGate();

                Serial.println("Bottle detected at color station");
                changeState(SystemState::EVALUATE_COLOR);
            }
            break;

        case SystemState::EVALUATE_COLOR:
            physicalColor = evaluateBottleColor();

            if (physicalColor == DetectedColor::RED) {
                Serial.println("Physical color: RED");
            } else if (physicalColor == DetectedColor::BLUE) {
                Serial.println("Physical color: BLUE");
            } else if (physicalColor == DetectedColor::GREEN) {
                Serial.println("Physical color: GREEN");
            } else if (physicalColor == DetectedColor::YELLOW) {
                Serial.println("Physical color: YELLOW");
            } else {
                Serial.println("Physical color: NONE");
            }

            changeState(SystemState::OUTPUT_CONTROL);
            break;

        case SystemState::OUTPUT_CONTROL:
            if (physicalColor == DetectedColor::RED || physicalColor == DetectedColor::BLUE) {
                Serial.println("Valid color. Moving to filling stage");
                openFillingGate();
                startMainConveyor(Config::MAIN_CONVEYOR_SPEED);
                changeState(SystemState::FILLING_ROUTING);
            } else {
                Serial.println("Invalid color. Sending to reject path");
                openRejectGate();
                startMainConveyor(Config::MAIN_CONVEYOR_SPEED);
                changeState(SystemState::QUALITY_REJECTED);
            }
            break;

        case SystemState::FILLING_ROUTING:
            if (physicalColor == DetectedColor::BLUE) {
                changeState(SystemState::FILL_BLUE);
            } else if (physicalColor == DetectedColor::RED) {
                changeState(SystemState::FILL_RED);
            } else {
                changeState(SystemState::QUALITY_REJECTED);
            }
            break;

        case SystemState::FILL_BLUE:
    
            break;

        case SystemState::FILL_RED:
            
            break;

        case SystemState::QUALITY_CONTROL:
            
            break;

        case SystemState::QUALITY_ACCEPTED:
            
            break;

        case SystemState::QUALITY_REJECTED:
            
            break;
    }
}


// >>>>>>>>>>>>>>>>>>>> Utility functions <<<<<<<<<<<<<<<<<<<<

void changeState(SystemState newState) {
    currentState = newState;
    stateStartTime = millis();
}

bool isSensorActive(uint8_t pin) {
    return digitalRead(pin) == Config::SENSOR_ACTIVE;
}

bool hasElapsed(unsigned long startTime, unsigned long duration) {
    return millis() - startTime >= duration;
}