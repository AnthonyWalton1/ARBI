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
// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS 38
#define TEMPERATURE_PRECISION 12

/********************************************************
 * PID Basic Example
 * Reading analog input 0 to control analog PWM output 3
 ********************************************************/

#include "PID_v1.h"

#define PIN_INPUT 0
#define PIN_OUTPUT 3

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

// arrays to hold device addresses must be apdated if more devices added
DeviceAddress Address0, Address1, Address2, Address3;

float Temp_0, Temp_1, Temp_2, Temp_3;
uint8_t Address_0, Address_1, Address_2, Address_3;

Hbridgepwm PELT(1); // set up the pelt object to control pelter one 
Hbridgepwm PELTo(2); // set up the pelt object to control pelter two
//Define Variables we'll be connecting to
double Setpoint, Input, Output;
double Setpoint2, Input2, Output2;

//Specify the links and initial tuning parameters
double Kp=100, Ki=0.8, Kd=0.01;
double Kp2=100, Ki2=0.8, Kd2=0.01;

float Temp_Avg = 0;
float Temp_Avg2=0;
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);
PID myPIDo(&Input2, &Output2, &Setpoint2, Kp2, Ki2, Kd2, DIRECT);


void setup() {
  // setup code
PELT.begin(9,22,23); // set up the hardware for the temperature pelter.
PELTo.begin(10,24,25);





// must have a large setup here for the temperature sensing device.
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

    //initialize the variables we're linked to
  sensors.requestTemperatures();
  Setpoint = 32;
  Setpoint2 =25;

  //turn the PID on
  myPID.SetMode(AUTOMATIC);
  myPIDo.SetMode(AUTOMATIC);
  

}
//************************************************************************************************************************
// start of main loop
//**************************************************************************************************************************


void loop() {
  // put your main code here, to run repeatedly:
  
  // debug code
  Serial.print("Requesting temperatures...");
  delay(1000);
  sensors.requestTemperatures();
  Serial.println("DONE");

  // print the device information
  printData(Address0);
  printData(Address1); 
  printData(Address2);
  printData(Address3);

 // end debug code.

  
  // set variables including device information
  Temp_0 = sensors.getTempC(Address0);
  Temp_1 = sensors.getTempC(Address1);
  Temp_2 = sensors.getTempC(Address2);
  Temp_3 = sensors.getTempC(Address3);
// PID one for pelter connected to ...
  Temp_Avg = Temp_0 + Temp_1;
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
  // end


// PID two for pelter connected to ...
    Temp_Avg2 = Temp_2 + Temp_3;
  Input2 = 0.25 * Temp_Avg2;
  Serial.print("Average Temperature 2 is ");
  Serial.println(Input2);
  myPID.Compute();
  Serial.print("Temperatures difference is ");
  Serial.println(Input2-Setpoint2);
  Serial.print("Output value for H-Bridge is ");
  Serial.println(Output2);
  PELT.hardwareprotect(Output2);
  PELT.set_pwm(Output2);
// end








  
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

