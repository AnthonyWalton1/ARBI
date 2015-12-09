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
double Setpoint, Input, Output; // setpoint is the wanted temperature in degrees celcius 
double Setpoint2, Input2, Output2; // setpoint 2 is the wanted temperature in degress celcius

//Specify the links and initial tuning parameters
double Kp=100, Ki=0.8, Kd=0.01;
double Kp2=100, Ki2=0.8, Kd2=0.01;

float Temp_Avg = 0;
float Temp_Avg2=0;
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);
PID myPIDo(&Input2, &Output2, &Setpoint2, Kp2, Ki2, Kd2, DIRECT);
volatile long int frequency_divder =5; // this variable is used to give the output frequency of the first pwm layer by divideing the base output frequency (~2500 hz), note must be at least 3
volatile long int frequency_count =1; // this variable is compared against the above.
volatile long int frequency_set=5;
volatile int frequency_divder2 =1; // this variable is used to give the output frequency of the first pwm layer by divideing the base output frequency (~2500 hz), note must be at least 3
volatile int state =1; // used to keep track of wheater the pwm is on or off. is set to one as it set on in the setupt function.


// setup for the uart comuincation:
// setup of serial communication between arduino and raspberry pi.
String inputString;        // a string to hold incoming data
String inputString2;
boolean stringComplete = 0;  // whether the string is complete
int variable_ID=0; // used to state which vairable the pi wishes to access
int ID_1=0;
int ID_2=0;
int variable_value =0; 
int vv_1=0;
int vv_2=0;
int vv_3=0;
bool invalid =0; // used to keep track of wheater the last message sent was invalid.
bool send_message=0; // used to define wheater message need to be send

void setup() {
  // setup code
PELT.begin(9,22,23,95,29,28); // set up the hardware for the temperature pelter.
PELTo.begin(10,24,25,94,30,31);
// reserve space for the input buffers
inputString.reserve(100);
inputString2.reserve(100);
 // start serial port
  Serial.begin(9600);
  // Start up the sensor library
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

if (PELT.status(Output)==0){ // means hbridge is operational and we can set the value.
  PELT.set_pwm(Output); 
}
  // end

// PID two for pelter connected to ...
    Temp_Avg2 = Temp_2 + Temp_3;
  Input2 = 0.25 * Temp_Avg2;
  myPIDo.Compute();
  
if (PELTo.status(Output)==0){ // means hbridge is operational and we can set the value.
  PELTo.set_pwm(Output); 
}
  
// end
// check serial communication
serialEvent();

// send data if was asked to.
if (send_message ==1){
serial_send_setpoints();
send_message =0; // reset the send bool.
}

// end of main
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
if (frequency_set > frequency_count){
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
if (frequency_set > frequency_count){
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

void serialEvent() {
  // the serial events functions grabs all ascii character stored in the serial bufffer and gives it to a variable
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == 10) { // this states the type of trailing null used.
      
      // we have a complete message, need to do some work with this message.
    //  Serial.print("success"); // debug code
      recieve_uart ();
    }
  }
}

void recieve_uart (){
// this function will only be called when we are given a completed strin, this functio'sn purpose is to trhow the string if it is bad and act upon the string if it is good. 
// first test for possible ways the string is bad.
// too long...
inputString.trim(); // remove the carrage return and new line
// Serial.print(inputString.length()); // debug code


if (inputString.length() != 6) // length does not include trailing null.
{ // 9 is the length of all input strings so if not 9 is wrong
inputString =""; // empty the string
Serial.print("invalid\r\n");
Serial.flush(); // remove all chars in the buffer as it is wrong.
}
else
{
// the string passed first test, next must pull out values and do work with them.
// the setup of the string is (n_x\0) where n is variable number and x is variables value. 

// Serial.print("success2\n"); // debug code
 
inputString.trim(); // remove the null.
inputString2 = inputString;
inputString = ""; // empty the string to recieve the next message.
inputString2.toInt(); // convert it to an int

  ID_1 =  inputString2[0]-48 ;
  ID_2 =  inputString2[1]-48 ;
variable_ID = (ID_1)*10 +ID_2 ;
   vv_1 = inputString2[3]-48 ;
   vv_2 = inputString2[4] -48 ;
   vv_3 = inputString2[5] -48 ; // all the ascii values are converted to inetegrs.
variable_value = (vv_1)*100 + (vv_2)*10 + (vv_3) ; // turned the ASCII three charcters into the actal number that they represent.

// Serial.print(variable_ID); // debug code
// Serial.print("\n"); // debug code
// Serial.print(variable_value); // debug code


//the code now gets the ID and value out as ints that can be used in a simple case statment.
// This case stament can be made a lot smaller by making a function that does the if staments in it. 
switch (variable_ID) {
          case 1:
      //when vairable ID is one led pwm 1 is to be adjusted.
      // must test to make sure that the variable is within acceptable margin
      if (variable_value >= 0 &&variable_value <= 255)
      {
        // we have recieved a valid message do work to it.
      analogWrite(2,150); // led 1
      Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
       Serial.print("invalid\r\n");
        
      }
    
      
      break;
          case 2:
      //when vairable ID is two led pwm 2 is to be adjusted.
      
      if (variable_value >= 0 &&variable_value <= 255)
      {
        // we have recieved a valid message do work to it.
      analogWrite(3,150); // led 1
      Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
       Serial.print("invalid\r\n");
        
      }
    
      
      break;
          case 3:
      //when vairable ID is three led pwm 3 is to be adjusted.
      if (variable_value >= 0 &&variable_value <= 255)
      {
        // we have recieved a valid message do work to it.
      analogWrite(5,150); // led 1
      Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
       Serial.print("invalid\r\n");
        
      }
    
      
      break;
          case 4:
      //when vairable ID is four led pwm 4 is to be adjusted.
      if (variable_value >= 0 &&variable_value <= 255)
      {
        // we have recieved a valid message do work to it.
      analogWrite(6,150); // led 1
      Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
       Serial.print("invalid\r\n");
        
      }
    
      
      break;
          case 5:
      //when vairable ID is five led pwm 5 is to be adjusted.
      if (variable_value >= 0 &&variable_value <= 255)
      {
        // we have recieved a valid message do work to it.
      analogWrite(7,150); // led 1
      Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
       Serial.print("invalid\r\n");
        
      }
      
      break;
          case 6:
      //when vairable ID is six led pwm 6 is to be adjusted.
            if (variable_value >= 0 &&variable_value <= 255)
      {
        // we have recieved a valid message do work to it.
      analogWrite(8,150); // led 1
      Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
       Serial.print("invalid\r\n");
        
      }

      break;
               case 7:
      //when vairable ID is seven the first temperature setpoint is to be adjusted.
            if (variable_value >= 0 &&variable_value <= 30)
      {
        // we have recieved a valid message do work to it.
      Setpoint = variable_value;
      Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
       Serial.print("invalid\r\n");
        
      }

      
      break;
                  case 8:
      //when vairable ID is eight the second temperature setpoint is to be adjusted.
      //when vairable ID is seven the first temperature setpoint is to be adjusted.
            if (variable_value >= 0 &&variable_value <= 30)
      {
        // we have recieved a valid message do work to it.
      Setpoint2 = variable_value;
      Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
       Serial.print("invalid\r\n");
        
      }
      
      break;
                        case 9:
      //when vairable ID is nine the frequency divider value setpoint is to be adjusted.
      //when vairable ID is seven the first temperature setpoint is to be adjusted.
            if (variable_value >= 4 &&variable_value <= 999)
      {
        // we have recieved a valid message do work to it.
       noInterrupts(); // disable interrupts as the below code requires mutilpe clocls and can break the code is is interrupted halfway thourhg.
      frequency_divder=variable_value;
      frequency_set=frequency_divder*frequency_divder2; // update the frequency divider value
      interrupts();
      Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
       Serial.print("invalid\r\n");
        
      }
      break;
      case 10:
      if (variable_value >= 1 &&variable_value <= 999)
      {
      // must update the frequency value
      noInterrupts();
      frequency_divder2=variable_value;
      frequency_set=frequency_divder*frequency_divder2; // update the frequency divider value
      interrupts();
       Serial.print("ack\r\n");   
      }
      else {
         Serial.print("invalid\r\n");
      }

      
      break;
      case 99:
      if (variable_value ==0){
      send_message =1;
     }
     else{
       Serial.print("invalid\r\n");
     }

     break;
        
    default: 
    // is nothing matches then we have recieved an invalid message, do nothing. // set invalid to one.   
    Serial.print("invalid\r\n"); 

    break;
  }

}

}

void serial_send_setpoints(){
  if(Setpoint <10){
Serial.print("07_00");
Serial.print((int)Setpoint);
Serial.print("\r\n");
}
else
{
Serial.print("07_0");
Serial.print((int)Setpoint);
Serial.print("\r\n");
}

if(Setpoint2 <10){
Serial.print("08_00");
Serial.print((int)Setpoint2);
Serial.print("\r\n");
}
else
{
Serial.print("08_0");
Serial.print((int)Setpoint2);
Serial.print("\r\n");
}


if (frequency_divder<10){
Serial.print("09_00");
Serial.print(frequency_divder);
Serial.print("\r\n");
}
else if(frequency_divder<100) {
Serial.print("09_0");
Serial.print(frequency_divder);
Serial.print("\r\n");
}
else {
Serial.print("09_");
Serial.print(frequency_divder);
Serial.print("\r\n");
}

if (frequency_divder2<10){
Serial.print("10_00");
Serial.print(frequency_divder2);
Serial.print("\r\n");
}
else if(frequency_divder2<100) {
Serial.print("10_0");
Serial.print(frequency_divder2);
Serial.print("\r\n");
}
else {
Serial.print("10_");
Serial.print(frequency_divder2);
Serial.print("\r\n");
}

}
// information for serial communication
// 01 to 06 set pwm frquencies for respective pwm
// 07 sets tempaerture setpoint 1
// 08 sets temperature setpoint 2
// 09 set frequency divder one
// 10 sets frequency divder two
// the frequency is given by 2500hz/ (frequency_divider_one * freqeucny_divider_two); 



