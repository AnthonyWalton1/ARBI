// Include the libraries we need
#include <OneWire.h>
#include <DallasTemperature.h>
#include "Arduino.h"
// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS 38
#define TEMPERATURE_PRECISION 12

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

// arrays to hold device addresses must be apdated if more devices added
DeviceAddress Address0, Address1, Address2, Address3;

float Temp_0, Temp_1, Temp_2, Temp_3;
uint8_t Address_0, Address_1, Address_2, Address_3;

void setup(void)
{
  // start serial port
  Serial.begin(9600);
  Serial.println("Algae Culture Box");

  // Start up the library
  sensors.begin();

  // locate devices on the bus
  Serial.print("Locating devices...");
  Serial.print("Found ");
  Serial.print(sensors.getDeviceCount(), DEC);
  Serial.println(" devices.");

  // report parasite power requirements
  Serial.print("Parasite power is: "); 
  if (sensors.isParasitePowerMode()) Serial.println("ON");
  else Serial.println("OFF");

  // Must be called before search()
  oneWire.reset_search();
  // assigns the first address found to insideThermometer
  if (!oneWire.search(Address0)) Serial.println("Unable to find address for first Thermometer");
  // assigns the second address found to middleThermometer
  if (!oneWire.search(Address1)) Serial.println("Unable to find address for second Thermometer");
  // assigns the third address found to outsideThermometer
  if (!oneWire.search(Address2)) Serial.println("Unable to find address for third Thermometer");
  // assigns the fourth address found to fourthThermometer
  if (!oneWire.search(Address3)) Serial.println("Unable to find address for fourth Thermometer");
  
  // show the addresses we found on the bus. Update addresses for added devices.
  Serial.print("Device 0 Address: ");
//  printAddress(Address0);
  Serial.println();

  Serial.print("Device 1 Address: ");
//  printAddress(Address1);
  Serial.println();

  Serial.print("Device 2 Address: ");
//  printAddress(Address2);
  Serial.println();

  Serial.print("Device 3 Address: ");
//  printAddress(Address3);
  Serial.println();

  // set the resolution to 12 bit per device. 
  sensors.setResolution(Address0, TEMPERATURE_PRECISION);
  sensors.setResolution(Address1, TEMPERATURE_PRECISION);
  sensors.setResolution(Address2, TEMPERATURE_PRECISION);
  sensors.setResolution(Address3, TEMPERATURE_PRECISION);
  
  Serial.print("Device 0 Resolution: ");
  Serial.print(sensors.getResolution(Address0), DEC); 
  Serial.println();

  Serial.print("Device 1 Resolution: ");
  Serial.print(sensors.getResolution(Address1), DEC); 
  Serial.println();

  Serial.print("Device 2 Resolution: ");
  Serial.print(sensors.getResolution(Address2), DEC); 
  Serial.println();

  Serial.print("Device 2 Resolution: ");
  Serial.print(sensors.getResolution(Address3), DEC); 
  Serial.println();
}
// function to print a device address
void printAddress(DeviceAddress deviceAddress)
{
  for (uint8_t i = 0; i < 8; i++)
  {
    // zero pad the address if necessary
    if (deviceAddress[i] < 16) Serial.print("0");
    Serial.print(deviceAddress[i], HEX);
  }
}

// function to print the temperature for a device
void printTemperature(DeviceAddress deviceAddress)
{
  float tempC = sensors.getTempC(deviceAddress);
  Serial.print("Temp C: ");
  Serial.print(tempC);
//  Serial.print(" Temp F: ");
// Serial.print(DallasTemperature::toFahrenheit(tempC));
}

// function to print a device's resolution
void printResolution(DeviceAddress deviceAddress)
{
  Serial.print("Resolution: ");
  Serial.print(sensors.getResolution(deviceAddress));
  Serial.println();    
}

// main function to print information about a device
void printData(DeviceAddress deviceAddress)
{
  Serial.print("Device Address: ");
  printAddress(deviceAddress);
  Serial.print(" ");
  printTemperature(deviceAddress);
  Serial.println();
}

void loop(void)
{ 
  // call sensors.requestTemperatures() to issue a global temperature 
  // request to all devices on the bus
  //  delay(10000); // added delay for temp measurements  
  Serial.print("Requesting temperatures...");
  sensors.requestTemperatures();
  Serial.println("DONE");

  // print the device information
  printData(Address0);
  printData(Address1); 
  printData(Address2);
  printData(Address3);
  
  // set variables including device information
  Temp_0 = sensors.getTempC(Address0);
  Temp_1 = sensors.getTempC(Address1);
  Temp_2 = sensors.getTempC(Address2);
  Temp_3 = sensors.getTempC(Address3);
}

