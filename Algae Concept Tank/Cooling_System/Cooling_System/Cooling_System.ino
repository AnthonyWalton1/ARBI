// this is the H bridge pwm set class
// it is a class that the value given by the pid function as the input and sets the pwm on the respective pin
// note the pin numbers in this device are hard coded not dynamically changed as should only need one or 2 h bridge in the circuit.

// to use this pwm set program
// first call begin (this sets up the function should only be called once)
// next call hardware protect once we have a pid value
// then call status
// then call set, if status was OK
// include the liberaires that you need.
#include "Hbridgepwm.h"
#include <OneWire.h>
#include <DallasTemperature.h>
#include "Temp_Sensor.h"
#include <PID_v1.h>

#define PIN_INPUT 0
#define PIN_OUTPUT 3

// Data wire is plugged into pin on the Arduino allows for multiple buses to be defined in Temp_Sensor_Borad.h
OneWire* busses[ONEWIRE_BUS_COUNT];
DallasTemperature* temps[ONEWIRE_BUS_COUNT];

/********************************************************
 * PID Basic Example
 * Reading analog input 0 to control analog PWM output 3
 ********************************************************/
//Define Variables we'll be connecting to
double Setpoint, Input, Output;

//Specify the links and initial tuning parameters
double Kp=100, Ki=0.8, Kd=0.01;
float Temp_Avg = 0;
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

/***************************************************************
THERMOMETERS Create new variables within structures defined in Temp_Sensor.h
***************************************************************/
SoftwareSerial* debug;
Stream* data;

device_data upload;
device_info start_delim;
device_info end_delim;
uint8_t retry_count = 0;

/*******************************************************************
 HBRIDGE Define object for peltier from PELT class 
************************************************88888***************/
 
Hbridgepwm PELT(1); // set up the pelt object for the hbridgepwm class 

/******************************************************************************************************************************
 pre-declaration
******************************************************************************************************************************/



/***********************************************************************
 the pre intialiser is finished next we must define the functions.
************************************************************************/

void setup() {
 
  PELT.begin(); // set up the hardware for the temperature pelter.
  uint8_t *buf = (uint8_t *)&start_delim;
  uint8_t *buf2 = (uint8_t *)&end_delim;
  for(uint16_t i = 0; i < sizeof(device_info); i++)
  {
    buf[i] = i;
    buf2[sizeof(device_info) - i - 1] = i;
  }
  Serial.begin(9600);
  data = &Serial;  
  Serial.println("Algae Culture Box");
  Serial.println("Starting...");
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

  busses[0] = new OneWire(ONE_WIRE_BUS_ONE_PIN);
  busses[1] = new OneWire(ONE_WIRE_BUS_TWO_PIN);
  temps[0] = new DallasTemperature(busses[0]);
  temps[1] = new DallasTemperature(busses[1]);  

  //initialize the variables we're linked to
  sensors.requestTemperatures();
  Setpoint = 32;

  //turn the PID on
  myPID.SetMode(AUTOMATIC);
  

}
//************************************************************************************************************************
// start of main loop
//**************************************************************************************************************************


void loop() {

  clear_input();

  if(!repeat(&temp_display, 5, 100))
  {
 //   Serial.println("Failed to send data.");
  }
  
//PELT.hardwareprotect(250);
// PELT.set_pwm(250);
   // call sensors.requestTemperatures() to issue a global temperature 
  // request to all devices on the bus
  //  delay(10000); // added delay for temp measurements  
//  Serial.print("Requesting temperatures...");
//  delay(1000);
//  sensors.requestTemperatures();
//  Serial.println("DONE");

//  // print the device information
//  printData(Address0);
//  printData(Address1); 
//  printData(Address2);
//  printData(Address3);
//  
//  // set variables including device information
//  Temp_0 = sensors.getTempC(Address0);
//  Temp_1 = sensors.getTempC(Address1);
//  Temp_2 = sensors.getTempC(Address2);
//  Temp_3 = sensors.getTempC(Address3);

  Temp_Avg = Temp_0 + Temp_1 + Temp_2 + Temp_3;
  Input = 0.25 * Temp_Avg;
  Serial.print("Average Temperature is ");
  Serial.println(Input);
  myPID.Compute();
  Serial.print("Temperatures difference is ");
  Serial.println(Input-Setpoint);
  Serial.print("Output value for H-Bridge is ");
  Serial.println(Output);
  PELT.hardwareprotect(Output);
  PELT.set_pwm(Output);
}



//*******************************************************************************************
// end of main loop
//*********************************************************************************************


// local function definitions
void printAddress(DeviceAddress deviceAddress)
{
  for (uint8_t i = 0; i < 8; i++)
  {
    // zero pad the address if necessary
    if (deviceAddress[i] < 16) Serial.print("0");
    Serial.print(deviceAddress[i], HEX);
  }
}

//// function to print the temperature for a device
//void printTemperature(DeviceAddress deviceAddress)
//{
//  float tempC = sensors.getTempC(deviceAddress);
//  Serial.print("Temp C: ");
//  Serial.print(tempC);
//  Serial.print(" Temp F: ");
// Serial.print(DallasTemperature::toFahrenheit(tempC));
}

//// function to print a device's resolution
//void printResolution(DeviceAddress deviceAddress)
//{
//  Serial.print("Resolution: ");
//  Serial.print(sensors.getResolution(deviceAddress));
//  Serial.println();    
//}

//// main function to print information about a device
//void printData(DeviceAddress deviceAddress)
//{
//  Serial.print("Device Address: ");
//  printAddress(deviceAddress);
//  Serial.print(" ");
//  printTemperature(deviceAddress);
//  Serial.println();
//}

void clear_input()
{
  while(data->available())
  {
    data->read();
  }
}

bool temp_display(int repeat_count)
{
  data->write((uint8_t*)&start_delim, sizeof(device_info));
  upload.temperature_count = 0;
//  delay(3500); // Measures bus 1 waits 750ms for conversion measure bus 2 wait 750ms for conversion then delay 3500ms to make delay total of 5seconds MUST CHANGE DELAY TO 4250ms IF ONLY RUNNING ONE BUS
  for(int i = 0; i < ONEWIRE_BUS_COUNT; i++)
  {
    temps[i]->begin();
    temps[i]->requestTemperatures();
  }
  for(int i = 0; i < ONEWIRE_BUS_COUNT; i++)
  {
//    delay(4250); // measure bus 1 wait 750ms for conversion delay 4250ms for 5 second delay and then measure bus 2 following same schedule
    Serial.print("Displaying Bus: ");
    Serial.println(i);
    display_bus(i);
  }

  Serial.print("Temperature Count: ");
  Serial.println(upload.temperature_count);
  Serial.println();

  data->write((uint8_t*)&end_delim, sizeof(device_info));
}

void display_bus(uint8_t bus)
{
  busses[bus]->reset_search();
  uint8_t address[8];

  while(busses[bus]->search(address))
  {
    if (OneWire::crc8(address, 7) == address[7]) {

      switch(address[0])
      {
        case 0x28:
        case 0x10:
          display_temperature(bus, address);
          break;
        case 0x30:
        default:
          break;
      }
    }else
    {
      Serial.println("Error");
    }
  }
}

void display_temperature(uint8_t bus, uint8_t *address)
{

  device_info record;
  record.value = temps[bus]->getTempC(address);
  memcpy(&record.address, address, 8); //This changed the output garbage
  if(temps[bus]->getResolution(address) != 12)
  {
    temps[bus]->setResolution(address, 12);
  }

  data->write((uint8_t*)&record, sizeof(device_info));

  Serial.print(' ');
  display_address(debug, address);
  Serial.print(' ');
  Serial.println(record.value);
  upload.temperature_count++;
}

void display_address(Stream* stream, uint8_t *address)
{
  for(int i = 0; i < 8; i++)
  {
    if(address[i] < 0x10)
    {
      Serial.print(0, HEX);
    }
    Serial.print(address[i], HEX);
  }
}

bool repeat(bool (*func)(int repeat_count), uint32_t count, uint32_t delayms)
{
  for(uint32_t i = 0; i < count; i++)
  {
    if(func(i))
    {
      return true;
    }
    delay(delayms);
  }
  return false;
}


