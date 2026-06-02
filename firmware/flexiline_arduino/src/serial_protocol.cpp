#include "serial_protocol.h"
#include "config.h"

SerialCommand readSerialCommand() {
    if (Serial.available() <= 0) {
        return SerialCommand::NONE;
    }

    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.length() == 0) {
        return SerialCommand::NONE;
    }

    if (command == Config::CMD_START) {
        return SerialCommand::START;
    }

    if (command == Config::CMD_STOP) {
        return SerialCommand::STOP;
    }

    if (command == Config::CMD_CAMERA_BLUE) {
        return SerialCommand::CAMERA_BLUE;
    }

    if (command == Config::CMD_CAMERA_RED) {
        return SerialCommand::CAMERA_RED;
    }

    if (command == Config::CMD_CAMERA_NONE) {
        return SerialCommand::CAMERA_NONE;
    }

    return SerialCommand::NONE;
}

void sendControlRequest() {
    Serial.println(Config::CMD_CONTROL_REQUEST);
}