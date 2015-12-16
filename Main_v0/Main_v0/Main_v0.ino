#include <Dhcp.h>
#include <Dns.h>
#include <Ethernet.h>
#include <EthernetClient.h>
#include <EthernetServer.h>
#include <EthernetUdp.h>

// this is main V0, Hbridge, PID, flowmeter, temperature sensor, uart comunication, frequency divider are all implemented
// to do add a way t get bigger frequency count values.
#include "Hbridgepwm.h"
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#define DS3231_I2C_ADDRESS 0x68

// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS 38
#define TEMPERATURE_PRECISION 12

#include "PID_v1.h"
#define PIN_INPUT 0
#define PIN_OUTPUT 3

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

// arrays to hold device addresses must be apdated if more devices added, 8 sensor locations are required.
DeviceAddress Address0, Address1, Address2, Address3, Address4, Address5, Address6, Address7, Address8;

float Temp_1=0, Temp_2=0, Temp_3=0, Temp_4=0, Temp_5=0, Temp_6=0, Temp_7=0, Temp_8=0;
uint8_t Address_0, Address_1, Address_2, Address_3, Address_4, Address_5, Address_6, Address_7, Address_8;

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

// the frequency controll variables.
volatile unsigned  long frequency_count =1; // this variable is compared against the above.
volatile unsigned  long frequency_divider_on_1=228;
volatile unsigned  long  frequency_divider_off_1=228;
volatile unsigned  long  period_value_on=91;// used to solve for the period (in seconds) of the high and low frequencies. 
volatile unsigned  long  period_value_off=91;// used to solve for the period (in seconds) of the high and low frequencies. 
volatile bool state =1; // used to keep track of wheater the pwm is on or off. is set to one as it set on in the setupt function.
volatile byte on_off = 0; //used to keep track of wheater the leds are on or off.

// setup for the uart comuincation:
// setup of serial communication between arduino and raspberry pi.
String inputString;        // a string to hold incoming data
boolean stringComplete = 0;  // whether the string is complete
byte variable_ID=0; // used to state which vairable the pi wishes to access
byte ID_1=0;
byte ID_2=0;
long int variable_value =0; 
byte vv_1=0;
byte vv_2=0;
byte vv_3=0;
byte vv_4=0;
byte vv_5=0;
byte vv_6=0;
byte vv_7=0;
bool send_message=0; // used to define wheater message need to be send

// for the flow meter setup.
long int flow_counter=0; // this value is used to count real time for the flow meter approx a count of 5000 means 1 second has passed.
byte wait_for_measurment_counter=0; // will be used to slow to speed of calcualting the flow rate so a good number of data samples can be taken.
int number_of_spikes=1;
int liters_per_min_10_powerofone2 =0;

// for the RTC component.
byte second, minute, hour, dayOfWeek, dayOfMonth, month, year;
byte second_set=0;
byte minute_set =0;
byte hour_set=0;
byte day_of_week_set=0;
byte day_of_month_set=0;
byte month_set=0;
byte year_set=0;
// these values are used to update the RTC if necessary.

// for the RGB light sensors.
byte ledpwm1=150;
byte ledpwm2=150;
byte ledpwm3=150;
byte ledpwm4=150;
byte ledpwm5=150;
byte ledpwm6=150;
unsigned int red_1_setpoint=0;
unsigned int blue_1_setpoint=0;
unsigned int red_2_setpoint=0;
unsigned int blue_2_setpoint=0;
unsigned int red_3_setpoint=0;
unsigned int blue_3_setpoint=0;
unsigned int red_1_value=0;
unsigned int blue_1_value=0;
unsigned int red_2_value=0;
unsigned int blue_2_value=0;
unsigned int red_3_value=0;
unsigned int blue_3_value=0;

void setup() {
  
  // setup code
  PELT.begin(9,22,23,95,29,28); // set up the hardware for the first pelter module
  PELTo.begin(10,24,25,94,30,31); // set up the hardware for the second pelter module

  // reserve space for the input buffers
  inputString.reserve(15);

  // set up the interrupt for the flow counter.
  attachInterrupt(digitalPinToInterrupt(18), flow_meter_change, HIGH);

  // start serial port  
  Wire.begin();
  Serial.begin(9600);

  // Start up the sensor library
  sensors.begin();

  // locate the dallas temperature IC devices on the bus
  sensors.getDeviceCount();

  // Must be called before search()oneWire.reset_search();
  // assigns the first address found to insideThermometer
  if (!oneWire.search(Address0)) 
  // assigns the second address found to middleThermometer
  if (!oneWire.search(Address1)) 
  // assigns the third address found to outsideThermometer
  if (!oneWire.search(Address2))
  // assigns the fourth address found to fourthThermometer
  if (!oneWire.search(Address3))
  // assigns the fifth adress
  if (!oneWire.search(Address4)) 
  // assigns the sixth address found to middleThermometer
  if (!oneWire.search(Address5)) 
  // assigns the seventh address found to outsideThermometer
  if (!oneWire.search(Address6))
  // assigns the eigth address found to fourthThermometer
  if (!oneWire.search(Address7))

  // set the resolution to 12 bit per device. 
  sensors.setResolution(Address0, TEMPERATURE_PRECISION);
  sensors.setResolution(Address1, TEMPERATURE_PRECISION);
  sensors.setResolution(Address2, TEMPERATURE_PRECISION);
  sensors.setResolution(Address3, TEMPERATURE_PRECISION);
  sensors.setResolution(Address4, TEMPERATURE_PRECISION);
  sensors.setResolution(Address5, TEMPERATURE_PRECISION);
  sensors.setResolution(Address6, TEMPERATURE_PRECISION);
  sensors.setResolution(Address7, TEMPERATURE_PRECISION);

  //initialize the variables we're linked to
  sensors.requestTemperatures();
  // setup the PID temperature set points.
  Setpoint = 32;
  Setpoint2 =25;

  //turn the PID on
  myPID.SetMode(AUTOMATIC);
  myPIDo.SetMode(AUTOMATIC);

  // set up the pwm pins for the 6 led's to the highest frequency (approx 31khz)
  TCCR1B = TCCR1B & 0b11111000 | 0x02; // the frequency of the timer interrupt set on overflow interrupt.
  TCCR2B = TCCR2B & 0b11111000 | 0x01; // below are the frequency of the LED's
  TCCR3B = TCCR3B & 0b11111000 | 0x01;
  TCCR4B = TCCR4B & 0b11111000 | 0x01;
  TCCR5B = TCCR5B & 0b11111000 | 0x01;
  TIMSK0 = (0<<OCIE0A) | (1<<TOIE0); // enable the timer interrupt for timer unit 1.
  TIMSK1 = _BV(TOIE1); // enable overflow as the type of interrupt used.

  analogWrite(2,ledpwm1); // led 1 , turn the led's on.
  analogWrite(3,ledpwm2); // led 2
  analogWrite(5,ledpwm3); // led 3
  analogWrite(6,ledpwm4); // led 4
  analogWrite(7,ledpwm5); // led 5
  analogWrite(8,ledpwm6); // led 6
  
}

//************************************************************************************************************************
// start of main loop
//**************************************************************************************************************************

void loop() {
  
  // put your main code here, to run repeatedly:
  // to do, update pelter code for correct inputs of temperatures deices and to ignored bad data(85, -127 and 255 which are all error signals from the IC) 
  // make variables to hold the temperature ID's as these are need to identif the ones in the system.
  // request current sensor values.  
  sensors.requestTemperatures();  
  
  // set variables including device information
  Temp_1 = sensors.getTempC(Address1);
  Temp_2 = sensors.getTempC(Address2);
  Temp_3 = sensors.getTempC(Address3);
  Temp_4 = sensors.getTempC(Address4);
  Temp_5 = sensors.getTempC(Address5);
  Temp_6 = sensors.getTempC(Address6);
  Temp_7 = sensors.getTempC(Address7);

  // PID one for pelter connected to one
  Temp_Avg =  Temp_1;
  Input = 0.25 * Temp_Avg;
  myPID.Compute();

  if (PELT.status(Output)==0) { // means hbridge is operational and we can set the value.
    PELT.set_pwm(Output); 
  } else if (PELT.status(Output)==2) {
    PELT.set_pwm(0); // the hbridge has momentarily failed, turn it off so that it can have time to reset.  
  }

  // PID two for pelter connected to two
  Temp_Avg2 = Temp_2 + Temp_3; 
  Input2 = 0.25 * Temp_Avg2;
  myPIDo.Compute();
  
  if (PELTo.status(Output)==0){ // means hbridge is operational and we can set the value.
    PELTo.set_pwm(Output); 
  } else if (PELTo.status(Output)==2) {
    PELTo.set_pwm(0); // the hbridge has momentarily failed, turn it off so that it can have time to reset.  
  }

  // calculate the flow rate
  flow_rate_calculate();

  // check serial communication
  serialEvent();
  
  // send data if was asked to be sent
  serial_send_setpoints();

  // update the time with the RTC
  RTC_set();
  
}

//*******************************************************************************************
// end of main loop
//*********************************************************************************************



// *******************************************************************************************************************
ISR(TIMER1_OVF_vect) {
  
  // this is the interrupt service routine function (note as an interrupt function it can only see global varables)
  flow_counter=flow_counter+1; //update the flow counter so we know how much time occurs between the square wave signals.

  if (on_off ==0) { // ignores the rest of the code if the leds are set to a permanant state via serial communication.
    
    if (state ==0){ // the pwm is off, next must implement frequency divider
      
      if (frequency_divider_off_1 > frequency_count){  
        frequency_count = frequency_count +1; // update the count
      } else {
        analogWrite(2,ledpwm1); // led 1
        analogWrite(3,ledpwm2); // led 2
        analogWrite(5,ledpwm3); // led 3
        analogWrite(6,ledpwm4); // led 4
        analogWrite(7,ledpwm5); // led 5
        analogWrite(8,ledpwm6); // led 6
        frequency_count =1;  
        state =1;
      }
    }
    
    if (state ==1) { // the pwm is on, turn it off.
      
      if (frequency_divider_on_1 > frequency_count){
        frequency_count = frequency_count +1; // update the count 
      } else {
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
  
}

//************************************************************************************************************************

void serialEvent() {
  
  // the serial events functions grabs all ascii character stored in the serial bufffer and gives it to a string variable
  while (Serial.available()) {
    
    // get the new byte:
    char inChar = (char)Serial.read();
    
    // add it to the inputString:
    if (inputString.length() == 15){
      // have bad data, reset string and flush
      Serial.flush();
      inputString="";
    }
    
    inputString += inChar;
    
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == 10) { // this states the type of trailing null used.  
      // we have a complete message, need to do some work with this message.
      recieve_uart ();
    }
  }
  
}


void recieve_uart () {
  
  // this function will only be called when we are given a completed string, this function's purpose is to throw the string if it is bad and act upon the string if it is good. 
  // first test for possible ways the string is bad.
  
  // too long...
  inputString.trim(); // remove the carrage return
  inputString.trim(); // remove the new line
  
  // Serial.print(inputString.length()); // debug code
  
  // indent parts of string now so does not need to be done again, note is the string is too short values will be random but below code makes sure that such vaulues will never be implemented
  ID_1 =  inputString[0] - 48;
  ID_2 =  inputString[1] - 48;
  variable_ID = (ID_1)*10 + ID_2;
  vv_1 = inputString[3] - 48;
  vv_2 = inputString[4] - 48;
  vv_3 = inputString[5] - 48; // all the ascii values are converted to inetegrs.
  vv_4 = inputString[6] - 48;
  vv_5 = inputString[7] - 48;
  vv_6 = inputString[8] - 48; // all the ascii values are converted to inetegrs.
  vv_7 = inputString[9] - 48;

  if (inputString.length() ==10) {// this is the case to set the on or off period length.
 
    if ((int)variable_ID ==11) { // set the on time period
      
      // set the approprate frequency divider vairables.
      on_off =0 ;// are in frequency divider state.
      noInterrupts();
      period_value_on =  ( (vv_1)*1000000 +(vv_2)*100000 +(vv_3)*10000 +(vv_4)*1000 +(vv_5)*100 + (vv_6) *10 +(vv_7)*1) ;
      frequency_divider_on_1 = (int)(period_value_on*3.85);
      frequency_count=1; //reset the frequency count
      
      if (frequency_divider_on_1 <5){ // as an n value of 5 or less breake the code.
        frequency_divider_on_1=5;
      }

      //just incase want 2.7 hrs light straight away
      interrupts();
      // Serial.println(frequency_divider_on_1);
      //Serial.println("ack");
      
    } else if((int)variable_ID ==12) { // set the off time period
      
      // set the appropriate frequency divider variables.
      on_off =0 ;// are in frequency divider state.
      noInterrupts();
      period_value_off =  ((vv_1)*1000000 +(vv_2)*100000 +(vv_3)*10000 +(vv_4)*1000 +(vv_5)*100 + (vv_6) *10 +(vv_7)*1) ;
      frequency_divider_off_1 = (int)(period_value_off*3.85);

      if (frequency_divider_off_1 <5){ // as an n value of 5 or less breake the code.
        frequency_divider_off_1=5;
      }

      // just incase want 2.7 hrs dark straight away.
      frequency_count=1; // reset the frequency count
      interrupts();

      // Serial.println(frequency_divider_off_1);
      // Serial.println("ack");
      
    } else {
      
    // invalid 
    // Serial.print("invalid"); // undebug if error checking is wanted.
    
    }

  } else if (inputString.length() == 4) { // length does not include trailing null.
  
    // this is the case if want to set leds into either on mode or off mode.
    if(variable_ID ==13) {
      
      if(vv_1 ==1){ // this is permanently on state. 
         
        // write all the led's high.  
        on_off =1; //led are permanently on
        
        analogWrite(2,ledpwm1); // led 1
        analogWrite(3,ledpwm2); // led 2
        analogWrite(5,ledpwm3); // led 3
        analogWrite(6,ledpwm4); // led 4
        analogWrite(7,ledpwm5); // led 5
        analogWrite(8,ledpwm6); // led 6
        
      } else if(vv_1 ==2) { // this is permantly off state.

        // write all the LEDs low
        on_off =2; // leds are permantly off.
        
        // write all the led's low. 
        digitalWrite(2,LOW); // turn the pwm back off
        digitalWrite(3,LOW); // turn the pwm back off 
        digitalWrite(5,LOW); // turn the pwm back off 
        digitalWrite(6,LOW); // turn the pwm back off 
        digitalWrite(7,LOW); // turn the pwm back off 
        digitalWrite(8,LOW); // turn the pwm back off 
        
      } else if(vv_1 ==0) {
        
        // back into blinking mode (with previously set values)
        noInterrupts();
        
        on_off =0 ;// are in frequency divider state.
        
        frequency_count=1; // reset the frequency count
        frequency_divider_on_1 = (int)(period_value_on*2.5);
        frequency_divider_off_1 = (int)(period_value_off*2.5);
        interrupts();
        
      }
      
    }
    
  } else if (inputString.length() == 5) { // length does not include trailing null.
    
    // 9 is the length of all input strings so if not 9 is wrong
    variable_value = (vv_1)*10 +(vv_2)*1;
    
    if(variable_value <60 && variable_value >1) {      
      switch (variable_ID) {
        case 9:
  
          Setpoint=variable_value; 
          break;
          
        case 10:
        
          Setpoint2=variable_value; 
          break;
          
        default: 
        
          // is nothing matches then we have recieved an invalid message, do nothing. // set invalid to one.   
          // turn back on after debug  Serial.print("invalid\r\n");
          break;          
      }
    }

  } else if (inputString.length() == 6) { // length does not include trailing null.
    
    // 9 is the length of all input strings so if not 9 is wrong
    variable_value = (vv_1)*100 +(vv_2)*10 +(vv_3)*1;
 
    switch (variable_ID) { 
       
      case 99:  
      
        if (variable_value ==0) {
          send_message =1;
        } else {
          // turn back on after debug  Serial.print("invalid\r\n");
        }
        
        break; 
           
      default: 

        // is nothing matches then we have recieved an invalid message, do nothing. // set invalid to one.   
        // turn back on after debug  Serial.print("invalid\r\n");
        break;
        
    }
      
  } else if (inputString.length() == 8) { // length does not include trailing null.
      
    // 9 is the length of all input strings so if not 9 is wrong

    // the string passed first test, next must pull out values and do work with them.
    // the setup of the string is (n_x\0) where n is variable number and x is variables value. 

    // Serial.print("success2\n"); // debug code

    // hold code  if(variable_value <65535){
    variable_value = (vv_1)*10000 + (vv_2)*1000 + (vv_3)*100 +(vv_4)*10 +(vv_5)*1 ; // turned the ASCII three charcters into the actal number that they represent.
     
    if (variable_value <65535) {   
      switch (variable_ID) { 
        case 14:           
          blue_1_setpoint =variable_value; 
          break;           
        case 15:    
          blue_2_setpoint =variable_value; 
          break;           
        case 16:    
          blue_3_setpoint =variable_value; 
          break;           
        case 17:    
          red_1_setpoint =variable_value; 
          break;         
        case 18:    
          red_2_setpoint =variable_value; 
          break;          
        case 19:     
          red_3_setpoint =variable_value; 
          break;    
        default:            
          // is nothing matches then we have recieved an invalid message, do nothing. // set invalid to one.   
          // turn back on after debug  Serial.print("invalid\r\n");
          break;  
      } 
    }
    
  } else {  
           
    Serial.flush(); // is not given a knowen format flush the serial buffer.  
  
  }
       
  inputString = ""; // must empty the input string regardless of what it held once work is done on it.
  
}

 
void serial_send_setpoints() {
  
  if (send_message ==1){
    // first send the 8 temperature values.
    // see if you can shorten this, also make it so temp sending is x100 for the float not just int.
    shorten_serial((int)(Temp_1*100),1,4);
    shorten_serial((int)(Temp_2*100),2,4);
    shorten_serial((int)(Temp_3*100),3,4);
    shorten_serial((int)(Temp_4*100),4,4);
    shorten_serial((int)(Temp_5*100),5,4);
    shorten_serial((int)(Temp_6*100),6,4);
    shorten_serial((int)(Temp_7*100),7,4);
    shorten_serial((int)(Temp_8*100),8,4);
    shorten_serial(Setpoint,9,2);
    shorten_serial(Setpoint2,10,2);
    shorten_serial(period_value_on,11,7);
    shorten_serial(period_value_off,12,7);
    shorten_serial(on_off,13,1);
    shorten_serial(blue_1_setpoint,14,5);
    shorten_serial(blue_2_setpoint,15,5);
    shorten_serial(blue_3_setpoint,16,5);
    shorten_serial(red_1_setpoint,17,5);
    shorten_serial(red_2_setpoint,18,5);
    shorten_serial(red_3_setpoint,19,5);
    shorten_serial(blue_1_value,20,5);
    shorten_serial(blue_2_value,21,5);
    shorten_serial(blue_3_value,22,5);
    shorten_serial(red_1_value,23,5);
    shorten_serial(red_2_value,24,5);
    shorten_serial(red_3_value,25,5);
    shorten_serial(second,26,2);
    shorten_serial(minute,27,2);
    shorten_serial(hour,28,2);
    shorten_serial(dayOfMonth,29,2);
    shorten_serial(month,30,2);
    shorten_serial(year,31,2);
    shorten_serial(liters_per_min_10_powerofone2,32,3);
    Serial.println("\r\n"); // signifi end of message
    send_message =0; // reset the send bool.
  }
  
}

void flow_meter_change() { //ISR
  
  // counts whenever a new spike occurs.  
  number_of_spikes=number_of_spikes+1;

}

void flow_rate_calculate() {
  
  // this function is called to calculate the flow rate of the device.
  if (wait_for_measurment_counter>10) { // the function is only acted upon every 10 seconds or so to give a good amount of data to provide a decent estimate of the flow rate.
    
    wait_for_measurment_counter=0; 
    liters_per_min_10_powerofone2 = (int)round(((number_of_spikes/(flow_counter/5000))/7.5)*10); // this math calculates the liters per minute flow rate *10^2
    flow_counter=0;
    number_of_spikes=1; 
         
  } else {    
    wait_for_measurment_counter=wait_for_measurment_counter+1;
  }
  
}



//************************************************************************************************************************
// the below functions are used for the rtc component.
//************************************************************************************************************************


// Convert normal decimal numbers to binary coded decimal
byte decToBcd(byte val) {
  
  return( (val/10*16) + (val%10) );

}


// Convert binary coded decimal to normal decimal numbers
byte bcdToDec(byte val) {
  
  return( (val/16*10) + (val%16) );

}


void setDS3231time(byte second, byte minute, byte hour, byte dayOfWeek, byte
dayOfMonth, byte month, byte year) {
  
  // sets time and date data to DS3231
  Wire.beginTransmission(DS3231_I2C_ADDRESS);
  Wire.write(0); // set next input to start at the seconds register
  Wire.write(decToBcd(second)); // set seconds
  Wire.write(decToBcd(minute)); // set minutes
  Wire.write(decToBcd(hour)); // set hours
  Wire.write(decToBcd(dayOfWeek)); // set day of week (1=Sunday, 7=Saturday)
  Wire.write(decToBcd(dayOfMonth)); // set date (1 to 31)
  Wire.write(decToBcd(month)); // set month
  Wire.write(decToBcd(year)); // set year (0 to 99)
  Wire.endTransmission();

}


void readDS3231time(byte *second, byte *minute, byte *hour, byte *dayOfWeek,
byte *dayOfMonth, byte *month, byte *year) {
  
  Wire.beginTransmission(DS3231_I2C_ADDRESS);
  Wire.write(0); // set DS3231 register pointer to 00h
  Wire.endTransmission();
  Wire.requestFrom(DS3231_I2C_ADDRESS, 7);
  // request seven bytes of data from DS3231 starting from register 00h
  *second = bcdToDec(Wire.read() & 0x7f);
  *minute = bcdToDec(Wire.read());
  *hour = bcdToDec(Wire.read() & 0x3f);
  *dayOfWeek = bcdToDec(Wire.read());
  *dayOfMonth = bcdToDec(Wire.read());
  *month = bcdToDec(Wire.read());
  *year = bcdToDec(Wire.read());
  
}


void RTC_set() {
  
// get the current time.
  readDS3231time(&second, &minute, &hour, &dayOfWeek, &dayOfMonth, &month, &year);

}


// reduction of serial function
void shorten_serial(unsigned long int value, int ID, int length) { // lenght is correct length of string after _

  // this functions will simplify sending serial values.
  // first send ID.
  inputString = value;
  
  if (value >2147000000){
    value=0;
    inputString="0"; // block unlikely negative cases that would break the program.
  }

  if (ID <10){
    Serial.print("0");
    Serial.print(ID);
  } else {
  Serial.print(ID);
  }
  
  Serial.print("_");
  
  // next send the placeholding zeros
  while ((length - inputString.length()) > 0) {
    Serial.print("0"); // print a zero to give correct indentation.
    length=length-1;
  }

  //next send value and space.
  Serial.print(value);
  Serial.print(" ");
  inputString="";
  
}



//************************************************************************************************************************
// the below functions are for the updated temperature sensor code (auto increments all seen temperature sensors.)
//************************************************************************************************************************


///////////////////////////////////////////////// still to be implemented \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
// the light sensor code
// the advanced tempature sensor code with correct adressing
// the light find correct pwm code.
// simlifi code
/////////////////////////////////////////////////////////////end\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\





// decoding information about serial communication. \\

// for the temperature sensors.
// the temperature sensrs are given ID values of 30 -40. the data for a temparture sensor is 6 digits long, the first two digits (startting on the right) are 10 and 1s whilst the seond are 0.1s and 0.01s. The last two digits are the ID of the temperature device. 
// the are no decimals as the value is multiplies by 100 before hand, thus the value must be dived by 100 as a float to be correctly displayed.
//end
//for the frequency divider on the leds.(blinking controll not pwm controll)
// the frequency divider is controlled by 09_(on pulse time) and 10_(off pulse time). it has 9 digits. Thedigits determine how long the pulse is for.
// first digit (least signigicant (furthest right)) is ms, second is 10ms , third is 100ms. fourth is 1s, fifth is 10s, sixth is 100s, seventh is 1000s.
// the ninth digit detmines wheater led pulse on and off (0) or and permantly on (1) or are permanlty off (2)
//end
// for the luminosity sensor. the luminosity sensor outputs at 16digit binary (5 digit decimal) number that is proportional to the flux.
// there are three luminosity sensors. each outputs a lux values for R,G and B. this 9 ID are used for the light sensors.
// they are ID 40_50
//end
// for the RTC
// the RTC keeps track of time and sends a time stamp with every block of data send, the time stamp is 2 digits long and goes second, minute, hour, day of month, month, year.
// these values are given a sending ID of 15-20 for smallest to largest respectivly
// end.
  

