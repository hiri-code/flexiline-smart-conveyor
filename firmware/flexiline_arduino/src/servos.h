#pragma once

#include <Arduino.h>

void setupServos();

void resetServoPositions();

void openMainGate();
void closeMainGate();

void openFillingGate();
void closeFillingGate();

void openRejectGate();
void closeRejectGate();