#pragma once

#include <Arduino.h>

void setupServos();

void resetServoPositions();

void openMainGate();
void closeMainGate();

void openFillingGate();
void closeFillingGate();

void openPrimaryRejectGate();
void closePrimaryRejectGate();

void openFinalRejectGate();
void closeFinalRejectGate();