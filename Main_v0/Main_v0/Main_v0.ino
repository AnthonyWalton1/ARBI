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
volatile int frequency_divder =5; // this variable is used to give the output frequency of the first pwm layer by divideing the base output frequency (~2500 hz), note must be at least 3
volatile int frequency_count =1; // this variable is compared against the above.
volatile int state =1; // used to keep track of wheater the pwm is on or off. is set to one as it set on in the setupt function.
void setup() {
  // setup code
PELT.begin(9,22,23); // set up the hardware for the temperature pelter.
PELTo.begin(10,24,25);





// must have a large setup here for the temperature sensing device.
 // start serial port
  Serial.begin(9600);
  // Start up the library
  sensors.begin();

  // locate devices on the bus
sensors.getDeviceCount();

  // Must be called before search()
  oneWire.reset_search();
  // assigns the first address found to insideThermometer
  if (!oneWire.search(Address0)) 
  // assigns the second address found to middleThermometer
  if (!oneWire.search(Address1)) 
  // assigns the third address found to outsideThermometer
  if (!oneWire.search(Address2))
  // assigns the fourth address found to fourthThermometer
  if (!oneWire.search(Address3))
  

  // set the resolution to 12 bit per device. 
  sensors.setResolution(Address0, TEMPERATURE_PRECISION);
  sensors.setResolution(Address1, TEMPERATURE_PRECISION);
  sensors.setResolution(Address2, TEMPERATURE_PRECISION);
  sensors.setResolution(Address3, TEMPERATURE_PRECISION);
  

    //initialize the variables we're linked to
  sensors.requestTemperatures();
  Setpoint = 32;
  Setpoint2 =25;

  //turn the PID on
  myPID.SetMode(AUTOMATIC);
  myPIDo.SetMode(AUTOMATIC);

// set up the pwm pins for the 6 led's
TCCR1B = TCCR1B & 0b11111000 | 0x02;
TCCR2B = TCCR2B & 0b11111000 | 0x01;
TCCR3B = TCCR3B & 0b11111000 | 0x01;
TCCR4B = TCCR4B & 0b11111000 | 0x01;
TCCR5B = TCCR5B & 0b11111000 | 0x01; //set up the frequency divider registers
TIMSK0 = (0<<OCIE0A) | (1<<TOIE0); // enable the timer interrupt for timer unit 1.
TIMSK1 = _BV(TOIE1); // enable overflow as the type of interrupt used.
analogWrite(2,150); // led 1
analogWrite(3,150); // led 2
analogWrite(5,150); // led 3
analogWrite(6,150); // led 4
analogWrite(7,150); // led 5
analogWrite(8,150); // led 6

}
//************************************************************************************************************************
// start of main loop
//**************************************************************************************************************************


void loop() {
  // put your main code here, to run repeatedly:
 
  sensors.requestTemperatures();

  
  // set variables including device information
  Temp_0 = sensors.getTempC(Address0);
  Temp_1 = sensors.getTempC(Address1);
  Temp_2 = sensors.getTempC(Address2);
  Temp_3 = sensors.getTempC(Address3);
// PID one for pelter connected to ...
  Temp_Avg = Temp_0 + Temp_1;
  Input = 0.25 * Temp_Avg;

  myPID.Compute();
  PELT.hardwareprotect(Output);
  PELT.set_pwm(Output);
  // end

// PID two for pelter connected to ...
    Temp_Avg2 = Temp_2 + Temp_3;
  Input2 = 0.25 * Temp_Avg2;
  myPID.Compute();
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

ISR(TIMER1_OVF_vect){
// this is the interrupt service routine function (note as an interrupt function it can only see global varables)
if (state ==0){ // the pwm is off, next must implement frequency divider
if (frequency_divder != frequency_count){
frequency_count = frequency_count +1; // update the count
  
}
  else
  {
analogWrite(2,150); // led 1
analogWrite(3,150); // led 2
analogWrite(5,150); // led 3
analogWrite(6,150); // led 4
analogWrite(7,150); // led 5
analogWrite(8,150); // led 6
  frequency_count =1;  
  state =1;
  }
}
if (state ==1) { // the pwm is on, turn it off.
if (frequency_divder != frequency_count){
frequency_count = frequency_count +1; // update the count
  
}
  else
  {
digitalWrite(2,LOW); // turn the pwm back off and reset the count
digitalWrite(3,LOW); // turn the pwm back off and reset the count
digitalWrite(5,LOW); // turn the pwm back off and reset the count
digitalWrite(6,LOW); // turn the pwm back off and reset the count
digitalWrite(7,LOW); // turn the pwm back off and reset the count
digitalWrite(8,LOW); // turn the pwm back off and reset the count
  
  frequency_count =1;  
  state =0;
  }
} 
}


