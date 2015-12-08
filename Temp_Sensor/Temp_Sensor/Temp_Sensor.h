#ifndef _Temp_Sensor_H_
#define _Temp_Sensor_H_

#include "Arduino.h"
#include "OneWire.h"
#include "DallasTemperature.h"
#include "SoftwareSerial.h"

#include "Temp_Sensor_Board.h" // File to change pins as needed


#define ONEWIRE_BUS_COUNT 2 // number of buses running, have 2 buses at moment

#endif

bool temp_display(int repeat_count);

void display_bus(uint8_t bus); // confirm which bus is being used
void display_temperature(uint8_t bus, uint8_t *address); // display temperature associated with specific bus
void display_address(Stream* stream, uint8_t *address); // display device address
void display_address(Stream* stream, uint8_t *address); // display device address
void clear_input(); // clear input MAY NOT BE NEEDED

bool repeat(bool (*func)(int repeat_count), uint32_t count, uint32_t delayms); // boolean including function with parameters repeat_count, count and delayms

enum message_t
{
  DATA = 1,
  ERROR
};

struct device_info
{
  uint8_t address[8];
  double value;
};

struct device_data
{
  uint16_t temperature_count;
};

#ifdef __cplusplus
extern "C" {
#endif
void loop();
void setup();
#ifdef __cplusplus
}
#endif

