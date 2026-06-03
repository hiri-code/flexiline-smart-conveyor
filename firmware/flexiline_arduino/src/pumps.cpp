#include "pumps.h"
#include "config.h"

void setupPumps() {
    pinMode(Config::BLUE_PUMP_PIN, OUTPUT);
    pinMode(Config::RED_PUMP_PIN, OUTPUT);

    stopAllPumps();
}

void startBluePump() {
    digitalWrite(Config::BLUE_PUMP_PIN, Config::RELAY_ON);
}

void stopBluePump() {
    digitalWrite(Config::BLUE_PUMP_PIN, Config::RELAY_OFF);
}

void startRedPump() {
    digitalWrite(Config::RED_PUMP_PIN, Config::RELAY_ON);
}

void stopRedPump() {
    digitalWrite(Config::RED_PUMP_PIN, Config::RELAY_OFF);
}

void stopAllPumps() {
    stopBluePump();
    stopRedPump();
}