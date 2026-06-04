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

bool fillingStarted = false;
bool controlRequestSent = false;


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
    fillingStarted = false;
    controlRequestSent = false;

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
            closePrimaryRejectGate();
            closeFinalRejectGate();
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
                Serial.println("Invalid physical color. Sending to primary reject path");
            
                openPrimaryRejectGate();
                startMainConveyor(Config::MAIN_CONVEYOR_SPEED);
                changeState(SystemState::INITIAL_REJECT);
            }
            break;

        case SystemState::FILLING_ROUTING:
            if (physicalColor == DetectedColor::BLUE) {
                changeState(SystemState::FILL_BLUE);
            } else if (physicalColor == DetectedColor::RED) {
                changeState(SystemState::FILL_RED);
            } else {
                changeState(SystemState::INITIAL_REJECT);
            }
            break;

        case SystemState::FILL_BLUE:
            if (!fillingStarted && isSensorActive(Config::BLUE_FILL_SENSOR_PIN)) {
                Serial.println("Blue filling station reached");
            
                stopMainConveyor();
                closeFillingGate();
                startBluePump();
            
                fillingStarted = true;
                stateStartTime = millis();
            }
        
            if (
                fillingStarted &&
                hasElapsed(stateStartTime, Config::BLUE_FILLING_TIME_MS)
            ) {
                Serial.println("Blue filling complete");
            
                stopBluePump();
                startMainConveyor(Config::MAIN_CONVEYOR_SPEED);
            
                fillingStarted = false;
                changeState(SystemState::QUALITY_CONTROL);
            }
            break;

        case SystemState::FILL_RED:
            if (!fillingStarted && isSensorActive(Config::RED_FILL_SENSOR_PIN)) {
                Serial.println("Red filling station reached");
            
                stopMainConveyor();
                closeFillingGate();
                startRedPump();
            
                fillingStarted = true;
                stateStartTime = millis();
            }
        
            if (
                fillingStarted &&
                hasElapsed(stateStartTime, Config::RED_FILLING_TIME_MS)
            ) {
                Serial.println("Red filling complete");
            
                stopRedPump();
                startMainConveyor(Config::MAIN_CONVEYOR_SPEED);
            
                fillingStarted = false;
                changeState(SystemState::QUALITY_CONTROL);
            }
            break;

        case SystemState::QUALITY_CONTROL:
            if (!controlRequestSent && isSensorActive(Config::CAMERA_STATION_SENSOR_PIN)) {
                Serial.println("Bottle detected at camera station");
            
                stopMainConveyor();
                sendControlRequest();
            
                controlRequestSent = true;
                stateStartTime = millis();
            }
        
            if (controlRequestSent) {
                if (command == SerialCommand::CAMERA_BLUE) {
                    Serial.println("Camera result received: BLUE");
                    cameraColor = DetectedColor::BLUE;
                    startMainConveyor(Config::MAIN_CONVEYOR_SPEED);
                    changeState(SystemState::QUALITY_ACCEPTED);
                } else if (command == SerialCommand::CAMERA_RED) {
                    Serial.println("Camera result received: RED");
                    cameraColor = DetectedColor::RED;
                    startMainConveyor(Config::MAIN_CONVEYOR_SPEED);
                    changeState(SystemState::QUALITY_ACCEPTED);
                } else if (command == SerialCommand::CAMERA_NONE) {
                    Serial.println("Camera result received: NONE");
                    cameraColor = DetectedColor::NONE;
                    startMainConveyor(Config::MAIN_CONVEYOR_SPEED);
                    changeState(SystemState::FINAL_REJECT);
                }
            
                if (
                    currentState == SystemState::QUALITY_CONTROL &&
                    hasElapsed(stateStartTime, Config::CAMERA_RESPONSE_TIMEOUT_MS)
                ) {
                    Serial.println("Camera response timeout. Retrying CONTROL request.");
                    controlRequestSent = false;
                }
            }
            break;

        case SystemState::QUALITY_ACCEPTED:
            if (cameraColor == DetectedColor::BLUE) {
                startSorterConveyor(
                    Config::SORTER_CONVEYOR_SPEED,
                    MotorDirection::FORWARD
                );
            
                if (isSensorActive(Config::BLUE_OUTPUT_SENSOR_PIN)) {
                    Serial.println("Blue product routed successfully");
                
                    stopSorterConveyor();
                    changeState(SystemState::START_CONVEYOR);
                }
            } else if (cameraColor == DetectedColor::RED) {
                startSorterConveyor(
                    Config::SORTER_CONVEYOR_SPEED,
                    MotorDirection::REVERSE
                );
            
                if (isSensorActive(Config::RED_OUTPUT_SENSOR_PIN)) {
                    Serial.println("Red product routed successfully");
                
                    stopSorterConveyor();
                    changeState(SystemState::START_CONVEYOR);
                }
            } else {
                changeState(SystemState::FINAL_REJECT);
            }
            break;

        case SystemState::INITIAL_REJECT:
            if (
                isSensorActive(Config::REJECT_SENSOR_1_PIN) ||
                isSensorActive(Config::REJECT_SENSOR_2_PIN)
            ) {
                Serial.println("Primary reject completed");
            
                closePrimaryRejectGate();
                stopMainConveyor();
            
                changeState(SystemState::START_CONVEYOR);
            }
            break;

        case SystemState::FINAL_REJECT:
            openFinalRejectGate();

            startSorterConveyor(
                Config::SORTER_CONVEYOR_SPEED,
                MotorDirection::REVERSE
            );
        
            if (
                isSensorActive(Config::REJECT_SENSOR_1_PIN) ||
                isSensorActive(Config::REJECT_SENSOR_2_PIN)
            ) {
                Serial.println("Final reject completed");
            
                stopSorterConveyor();
                closeFinalRejectGate();
            
                changeState(SystemState::START_CONVEYOR);
            }
            break;
    }
}


// >>>>>>>>>>>>>>>>>>>> Utility functions <<<<<<<<<<<<<<<<<<<<

void changeState(SystemState newState) {
    currentState = newState;
    stateStartTime = millis();

    if (newState == SystemState::FILL_BLUE || newState == SystemState::FILL_RED) {
        fillingStarted = false;
    }

    if (newState == SystemState::QUALITY_CONTROL) {
        controlRequestSent = false;
        cameraColor = DetectedColor::NONE;
    }
}

bool isSensorActive(uint8_t pin) {
    return digitalRead(pin) == Config::SENSOR_ACTIVE;
}

bool hasElapsed(unsigned long startTime, unsigned long duration) {
    return millis() - startTime >= duration;
}