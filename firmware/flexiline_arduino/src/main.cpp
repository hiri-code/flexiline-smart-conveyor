#include <Arduino.h>

#include "config.h"
#include "serial_protocol.h"
#include "states.h"

void setup() {
    Serial.begin(Config::SERIAL_BAUD_RATE);
    Serial.setTimeout(Config::SERIAL_TIMEOUT_MS);

    Serial.println("FlexiLine firmware ready");
}

void loop() {
    SerialCommand command = readSerialCommand();

    switch (command) {
        case SerialCommand::START:
            Serial.println("START received");
            break;

        case SerialCommand::STOP:
            Serial.println("STOP received");
            break;

        case SerialCommand::CAMERA_BLUE:
            Serial.println("Camera result: BLUE");
            break;

        case SerialCommand::CAMERA_RED:
            Serial.println("Camera result: RED");
            break;

        case SerialCommand::CAMERA_NONE:
            Serial.println("Camera result: NONE");
            break;

        case SerialCommand::NONE:
        default:
            break;
    }
}