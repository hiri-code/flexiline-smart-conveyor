#pragma once

#include <Arduino.h>

#include "states.h"

void setupMotors();

void startMainConveyor(uint8_t speed);
void stopMainConveyor();

void startSorterConveyor(uint8_t speed, MotorDirection direction);
void stopSorterConveyor();

void stopAllMotors();