#include "color_sensor.h"

#include "config.h"

namespace {
    unsigned int readColorFrequency(uint8_t s2_state, uint8_t s3_state) {
        digitalWrite(Config::COLOR_SENSOR_S2_PIN, s2_state);
        digitalWrite(Config::COLOR_SENSOR_S3_PIN, s3_state);

        return pulseIn(Config::COLOR_SENSOR_OUT_PIN, LOW);
    }

    bool isYellow(unsigned int red, unsigned int green, unsigned int blue) {
        return (
            red > Config::COLOR_DIFFERENCE_THRESHOLD &&
            green > Config::COLOR_DIFFERENCE_THRESHOLD &&
            abs(static_cast<int>(red) - static_cast<int>(green)) < Config::YELLOW_BALANCE_THRESHOLD &&
            blue < red - Config::COLOR_DIFFERENCE_THRESHOLD &&
            blue < green - Config::COLOR_DIFFERENCE_THRESHOLD
        );
    }

    bool isRed(unsigned int red, unsigned int green, unsigned int blue) {
        return (
            red < blue - Config::COLOR_DIFFERENCE_THRESHOLD &&
            red < green - Config::COLOR_DIFFERENCE_THRESHOLD
        );
    }

    bool isBlue(unsigned int red, unsigned int green, unsigned int blue) {
        return (
            blue < red - Config::COLOR_DIFFERENCE_THRESHOLD &&
            blue < green - Config::COLOR_DIFFERENCE_THRESHOLD
        );
    }

    bool isGreen(unsigned int red, unsigned int green, unsigned int blue) {
        return (
            green < red - Config::COLOR_DIFFERENCE_THRESHOLD &&
            green < blue - Config::COLOR_DIFFERENCE_THRESHOLD
        );
    }
}

void setupColorSensor() {
    pinMode(Config::COLOR_SENSOR_S0_PIN, OUTPUT);
    pinMode(Config::COLOR_SENSOR_S1_PIN, OUTPUT);
    pinMode(Config::COLOR_SENSOR_S2_PIN, OUTPUT);
    pinMode(Config::COLOR_SENSOR_S3_PIN, OUTPUT);
    pinMode(Config::COLOR_SENSOR_OUT_PIN, INPUT);

    digitalWrite(Config::COLOR_SENSOR_S0_PIN, Config::COLOR_SENSOR_S0_STATE);
    digitalWrite(Config::COLOR_SENSOR_S1_PIN, Config::COLOR_SENSOR_S1_STATE);
}

DetectedColor evaluateBottleColor() {
    unsigned int red = 0;
    unsigned int green = 0;
    unsigned int blue = 0;

    for (uint8_t i = 0; i < Config::COLOR_SENSOR_SAMPLE_COUNT; ++i) {
        red += readColorFrequency(LOW, LOW);
        green += readColorFrequency(HIGH, HIGH);
        blue += readColorFrequency(LOW, HIGH);
    }

    red /= Config::COLOR_SENSOR_SAMPLE_COUNT;
    green /= Config::COLOR_SENSOR_SAMPLE_COUNT;
    blue /= Config::COLOR_SENSOR_SAMPLE_COUNT;

    if (isYellow(red, green, blue)) {
        return DetectedColor::YELLOW;
    }

    if (isRed(red, green, blue)) {
        return DetectedColor::RED;
    }

    if (isBlue(red, green, blue)) {
        return DetectedColor::BLUE;
    }

    if (isGreen(red, green, blue)) {
        return DetectedColor::GREEN;
    }

    return DetectedColor::NONE;
}