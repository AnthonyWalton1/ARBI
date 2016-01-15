// this is main V0, Hbridge, PID, flowmeter, temperature sensor, uart comunication, frequency divider are all implemented
#include "Hbridgepwm.h"
#include <OneWire.h>
#include <DallasTemperature.h>
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


// the frequency controll variables.
volatile unsigned  long  frequency_set_on =228; // this variable is used to give the output frequency (period) of the on part given by 2500hz/n where n must be 5 or greater.
volatile unsigned  long frequency_set_off=228; // this varible is used to give the putput frequency (period) of the off part given.
volatile unsigned  long frequency_count =1; // this variable is compared against the above.
volatile unsigned  long frequency_divider_on_1=0;
volatile unsigned  long  frequency_divider_off_1=0;
volatile unsigned  long  period_value_on=91;// used to solve for the period (in seconds) of the high and low frequencies. 
volatile unsigned  long  period_value_off=91;// used to solve for the period (in seconds) of the high and low frequencies. 
volatile bool state =1; // used to keep track of wheater the pwm is on or off. is set to one as it set on in the setupt function.
volatile bool stop_led_blinking =0;
short int on_off = 0; //used to keep track of wheater the leds are on or off.

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
int vv_4=0;
int vv_5=0;
int vv_6=0;
int vv_7=0;
int vv_8=0;
int vv_9=0;
bool invalid =0; // used to keep track of wheater the last message sent was invalid.
bool send_message=0; // used to define wheater message need to be send

int ledpwm1=150;
int ledpwm2=150;
int ledpwm3=150;
int ledpwm4=150;
int ledpwm5=150;
int ledpwm6=150;

// for the flow meter setup.
float flow_counter=0; // this value is used to count real time for the flow meter approx a count of 5000 means 1 second has passed.
int wait_for_measurment_counter=0; // will be used to slow to speed of calcualting the flow rate so a good number of data samples can be taken.
float number_of_spikes=1;
int liters_per_min_10_powerofone2 =0;



void setup() {
  // setup code
PELT.begin(9,22,23,95,29,28); // set up the hardware for the temperature pelter.
PELTo.begin(10,24,25,94,30,31);
// reserve space for the input buffers
inputString.reserve(100);
inputString2.reserve(100);
 // start serial port
// set up the interrupt for the flow counter.
attachInterrupt(digitalPinToInterrupt(18), flow_meter_change, HIGH);

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

analogWrite(2,ledpwm1); // led 1
analogWrite(3,ledpwm2); // led 2
analogWrite(5,ledpwm3); // led 3
analogWrite(6,ledpwm4); // led 4
analogWrite(7,ledpwm5); // led 5
analogWrite(8,ledpwm6); // led 6
// fixing the led pwm change bits
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
  
// PID one for pelter connected to one
  Temp_Avg = Temp_0 + Temp_1;
  Input = 0.25 * Temp_Avg;

  myPID.Compute();

if (PELT.status(Output)==0){ // means hbridge is operational and we can set the value.
  PELT.set_pwm(Output); 
}
else if (PELT.status(Output)==2){
  PELT.set_pwm(0); // the hbridge has momentarily failed, turn it off so that it can have time to reset.  
}
//end

// PID two for pelter connected to two
    Temp_Avg2 = Temp_2 + Temp_3;
  Input2 = 0.25 * Temp_Avg2;
  myPIDo.Compute();
  
if (PELTo.status(Output)==0){ // means hbridge is operational and we can set the value.
  PELTo.set_pwm(Output); 
}
  else if (PELTo.status(Output)==2){
  PELTo.set_pwm(0); // the hbridge has momentarily failed, turn it off so that it can have time to reset.  
}
// end

// calculate the flow rate
flow_rate_calculate();
//end

// check serial communication
serialEvent();
//end

// send data if was asked to be send
serial_send_setpoints();
// end
}

//*******************************************************************************************
// end of main loop
//*********************************************************************************************



// *******************************************************************************************************************
ISR(TIMER1_OVF_vect){
// this is the interrupt service routine function (note as an interrupt function it can only see global varables)
flow_counter=flow_counter+1; //update the flow counter so we know how much time occurs between the square wave signals.


if (stop_led_blinking ==0) { // we ignore the rest of the code)
if (state ==0){ // the pwm is off, next must implement frequency divider
if (frequency_set_off > frequency_count){
frequency_count = frequency_count +1; // update the count
  
}
  else
  {
   
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
if (frequency_set_on > frequency_count){
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
}

//************************************************************************************************************************

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
if (inputString.length() ==12) {// this is the case to set the on or off period length.
 
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
   vv_4 = inputString2[6]-48 ;
   vv_5 = inputString2[7] -48 ;
   vv_6 = inputString2[8] -48 ; // all the ascii values are converted to inetegrs.
   vv_7 = inputString2[9]-48 ;
   vv_8 = inputString2[10] -48 ;
   vv_9 = inputString2[11] -48 ; // all the ascii values are converted to inetegrs.


// we have the timer values that we set so we need to take them aprart to set the correct timing
if(vv_1 ==0) // case that we want to set a on off period. 
{
  on_off =0 ;// are in frequency divider state.
 stop_led_blinking =0; // let the leds blink at a set frequency
if ((int)variable_ID ==9) { // set the on time period
// set the approprate frequency divider vairables.
noInterrupts();
period_value_on =  ((vv_2)*10000000 +(vv_3)*1000000 +(vv_4)*100000 +(vv_5)*10000 +(vv_6)*1000 +(vv_7)*100 + (vv_8) *10 +(vv_9)*1) ;
frequency_divider_on_1 = (int)(period_value_on*2.5);
frequency_count=0; //reset the frequency count
frequency_set_on = frequency_divider_on_1;

 //just incase want 2.7 hrs ligh straight away
interrupts();
// Serial.println(frequency_divider_on_1);
//Serial.println("ack");
}

  
else if((int)variable_ID ==10) { // set the off time period
// set the appropriate frequency divider variables.
noInterrupts();
period_value_off = ((vv_2)*10000000 +(vv_3)*1000000 +(vv_4)*100000 +(vv_5)*10000 +(vv_6)*1000 +(vv_7)*100 + (vv_8) *10 +(vv_9)*1) ;
frequency_divider_off_1 = (int)(period_value_off*2.5);
frequency_set_off = frequency_divider_off_1;
 // just incase want 2.7 hrs dark straight away.
frequency_count=0; // reset the frequency count
interrupts();


// Serial.println(frequency_divider_off_1);
// Serial.println("ack");
}
  
else{
// invalid 
// Serial.print("invalid"); // undebug if error checking is wanted.
  
}
}
else if(vv_1 ==1){ // this is permanently on state.
stop_led_blinking =1; // stops the led from blinking by skipping most of the ISR function  
// write all the led's high.  
on_off =1; //led are permanently on
analogWrite(2,ledpwm1); // led 1
analogWrite(3,ledpwm2); // led 2
analogWrite(5,ledpwm3); // led 3
analogWrite(6,ledpwm4); // led 4
analogWrite(7,ledpwm5); // led 5
analogWrite(8,ledpwm6); // led 6
}
else if(vv_1 ==2){ // this is permantly off state.
stop_led_blinking=1; 
on_off =2; // leds are permantly off.
// write all the led's low. 
digitalWrite(2,LOW); // turn the pwm back off
digitalWrite(3,LOW); // turn the pwm back off 
digitalWrite(5,LOW); // turn the pwm back off 
digitalWrite(6,LOW); // turn the pwm back off 
digitalWrite(7,LOW); // turn the pwm back off 
digitalWrite(8,LOW); // turn the pwm back off 
}
}

else if (inputString.length() != 6) // length does not include trailing null.
{ // 9 is the length of all input strings so if not 9 is wrong
inputString =""; // empty the string
// Serial.print("invalid\r\n"); removed as error checking not relative, add if necessary.
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
        ledpwm1=variable_value;
      analogWrite(2,ledpwm1); // led 1
    // turn back on after debug  Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
     // turn back on after debug  Serial.print("invalid\r\n");
        
      }
    
      
      break;
          case 2:
      //when vairable ID is two led pwm 2 is to be adjusted.
      
      if (variable_value >= 0 &&variable_value <= 255)
      {
       ledpwm2=variable_value;
      analogWrite(3,ledpwm2); // led 1
         // turn back on after debug  Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
       // turn back on after debug  Serial.print("invalid\r\n");
        
      }
    
      
      break;
          case 3:
      //when vairable ID is three led pwm 3 is to be adjusted.
      if (variable_value >= 0 &&variable_value <= 255)
      {
        // we have recieved a valid message do work to it.
            ledpwm3=variable_value;
      analogWrite(5,ledpwm3); // led 1
         // turn back on after debug  Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
     // turn back on after debug  Serial.print("invalid\r\n");
        
      }
    
      
      break;
          case 4:
      //when vairable ID is four led pwm 4 is to be adjusted.
      if (variable_value >= 0 &&variable_value <= 255)
      {
        // we have recieved a valid message do work to it.
            ledpwm4=variable_value;
      analogWrite(6,ledpwm4); // led 1
        // turn back on after debug  Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
      // turn back on after debug  Serial.print("invalid\r\n");
        
      }
    
      
      break;
          case 5:
      //when vairable ID is five led pwm 5 is to be adjusted.
      if (variable_value >= 0 &&variable_value <= 255)
      {
        // we have recieved a valid message do work to it.
            ledpwm5=variable_value;
      analogWrite(7,ledpwm5); // led 1
         // turn back on after debug  Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
      // turn back on after debug  Serial.print("invalid\r\n");
        
      }
      
      break;
          case 6:
      //when vairable ID is six led pwm 6 is to be adjusted.
            if (variable_value >= 0 &&variable_value <= 255)
      {
        // we have recieved a valid message do work to it.
            ledpwm6=variable_value;
      analogWrite(8,ledpwm6); // led 1
         // turn back on after debug  Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
       // turn back on after debug  Serial.print("invalid\r\n");
        
      }

      break;
               case 7:
      //when vairable ID is seven the first temperature setpoint is to be adjusted.
            if (variable_value >= 0 &&variable_value <= 30)
      {
        // we have recieved a valid message do work to it.
      Setpoint = variable_value;
         // turn back on after debug  Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
        // turn back on after debug  Serial.print("invalid\r\n");
        
      }

      
      break;
                  case 8:
      //when vairable ID is eight the second temperature setpoint is to be adjusted.
      //when vairable ID is seven the first temperature setpoint is to be adjusted.
            if (variable_value >= 0 &&variable_value <= 30)
      {
        // we have recieved a valid message do work to it.
      Setpoint2 = variable_value;
        // turn back on after debug  Serial.print("ack\r\n");
      }
      else
      {
       // we have recieved an invalid messgae
       // turn back on after debug  Serial.print("invalid\r\n");
        
      }
      
      break;

      
      break;
      case 99:
      if (variable_value ==0){
      send_message =1;
     }
     else{
        // turn back on after debug  Serial.print("invalid\r\n");
     }

     break;
        
    default: 
    // is nothing matches then we have recieved an invalid message, do nothing. // set invalid to one.   
     // turn back on after debug  Serial.print("invalid\r\n");
 
    break;
  }

}

 }


void serial_send_setpoints(){
  if (send_message ==1){
if (ledpwm1<10){
Serial.print("01_00");
Serial.print(ledpwm1);
Serial.print(" ");
}
else if(ledpwm1<100) {
Serial.print("01_0");
Serial.print(ledpwm1);
Serial.print(" ");
}
else {
Serial.print("01_");
Serial.print(ledpwm1);
Serial.print(" ");
}

if (ledpwm2<10){
Serial.print("02_00");
Serial.print(ledpwm2);
Serial.print(" ");
}
else if(ledpwm2<100) {
Serial.print("02_0");
Serial.print(ledpwm2);
Serial.print(" ");
}
else {
Serial.print("02_");
Serial.print(ledpwm2);
Serial.print(" ");
}

if (ledpwm3<10){
Serial.print("03_00");
Serial.print(ledpwm3);
Serial.print(" ");
}
else if(ledpwm3<100) {
Serial.print("03_0");
Serial.print(ledpwm3);
Serial.print(" ");
}
else {
Serial.print("03_");
Serial.print(ledpwm3);
Serial.print(" ");
}

if (ledpwm4<10){
Serial.print("04_00");
Serial.print(ledpwm4);
Serial.print(" ");
}
else if(ledpwm4<100) {
Serial.print("04_0");
Serial.print(ledpwm4);
Serial.print(" ");
}
else {
Serial.print("04_");
Serial.print(ledpwm4);
Serial.print(" ");
}
if (ledpwm5<10){
Serial.print("05_00");
Serial.print(ledpwm5);
Serial.print(" ");
}
else if(ledpwm5<100) {
Serial.print("05_0");
Serial.print(ledpwm5);
Serial.print(" ");
}
else {
Serial.print("05_");
Serial.print(ledpwm5);
Serial.print(" ");
}

if (ledpwm6<10){
Serial.print("06_00");
Serial.print(ledpwm6);
Serial.print(" ");
}
else if(ledpwm6<100) {
Serial.print("06_0");
Serial.print(ledpwm6);
Serial.print(" ");
}
else {
Serial.print("06_");
Serial.print(ledpwm6);
Serial.print(" ");
}

  
  if(Setpoint <10){
Serial.print("07_00");
Serial.print((int)Setpoint);
Serial.print(" ");
}
else
{
Serial.print("07_0");
Serial.print((int)Setpoint);
Serial.print(" ");
}

if(Setpoint2 <10){
Serial.print("08_00");
Serial.print((int)Setpoint2);
Serial.print(" ");
}
else
{
Serial.print("08_0");
Serial.print((int)Setpoint2);
Serial.print(" ");
}


if(period_value_on <1){
Serial.print("09_00000000");
Serial.print((period_value_on));
Serial.print(" ");
}
else if(period_value_on <10){
Serial.print("09_00000000");
Serial.print((period_value_on));
Serial.print(" ");
}
else if(period_value_on <100){
Serial.print("09_0000000");
Serial.print((period_value_on));
Serial.print(" ");
}
else if(period_value_on <1000){
Serial.print("09_000000");
Serial.print((period_value_on));
Serial.print(" ");
}
else if(period_value_on <10000){
Serial.print("09_00000");
Serial.print((period_value_on));
Serial.print(" ");
}
else if(period_value_on <100000){
Serial.print("09_0000");
Serial.print((period_value_on));
Serial.print(" ");
}
else if(period_value_on <1000000){
Serial.print("09_000");
Serial.print((period_value_on));
Serial.print(" ");
}
else if(period_value_on <10000000){
Serial.print("09_00");
Serial.print((period_value_on));
Serial.print(" ");
}
else if(period_value_on <=999999999){
Serial.print("09_00");
Serial.print((period_value_on));
Serial.print(" ");
}


if(period_value_off <1){
Serial.print("10_00000000");
Serial.print((period_value_off));
Serial.print(" ");
}
else if(period_value_off <10){
Serial.print("10_00000000");
Serial.print((period_value_off));
Serial.print(" ");
}
else if(period_value_off <100){
Serial.print("10_0000000");
Serial.print((period_value_off));
Serial.print(" ");
}
else if(period_value_off <1000){
Serial.print("10_000000");
Serial.print((period_value_off));
Serial.print(" ");
}
else if(period_value_off <10000){
Serial.print("10_00000");
Serial.print((period_value_off));
Serial.print(" ");
}
else if(period_value_off <100000){
Serial.print("10_0000");
Serial.print((period_value_off));
Serial.print(" ");
}
else if(period_value_off <1000000){
Serial.print("10_000");
Serial.print((period_value_off));
Serial.print(" ");
}
else if(period_value_off <10000000){
Serial.print("10_00");
Serial.print((period_value_off));
Serial.print(" ");
}
else if(period_value_off <=9999999999){
Serial.print("10_00");
Serial.print((period_value_off));
Serial.print(" ");
}

if (liters_per_min_10_powerofone2<10){
Serial.print("11_00");
Serial.print(liters_per_min_10_powerofone2);
Serial.print(" ");

}
else if(liters_per_min_10_powerofone2<100) {
Serial.print("11_0");
Serial.print(liters_per_min_10_powerofone2);
Serial.print(" ");

}
else {
Serial.print("11_");
Serial.print(liters_per_min_10_powerofone2);
Serial.print(" ");

}
if ((int)(abs(Temp_Avg))<10){
Serial.print("12_00");
Serial.print((int)abs(Temp_Avg));
Serial.print(" ");

}
else if(((int)abs(Temp_Avg))<100) {
Serial.print("12_0");
Serial.print((int)abs(Temp_Avg));
Serial.print(" ");

}
else {
Serial.print("12_");
Serial.print((int)abs(Temp_Avg));
Serial.print(" ");
}
if ((int)(abs(Temp_Avg2))<10){
Serial.print("13_00");
Serial.print((int)abs(Temp_Avg2));
Serial.print(" ");
// Serial.print(" ");
}
else if(((int)abs(Temp_Avg2))<100) {
Serial.print("13_0");
Serial.print((int)abs(Temp_Avg2));
Serial.print(" ");
// Serial.print(" ");
}
else {
Serial.print("13_");
Serial.print((int)abs(Temp_Avg2));
Serial.print(" ");

}

if(on_off ==0){
Serial.print("14_000");
}
else if (on_off ==1){
Serial.print("14_001");  
}
else if (on_off ==2){
Serial.print("14_002");  
}

Serial.println("\r\n"); // signifi end of message
send_message =0; // reset the send bool.
}
}

void flow_meter_change() { //ISR
// counts whenever a new spike occurs.  
number_of_spikes=number_of_spikes+1;
}

void flow_rate_calculate(){
// this function is called to calculate the flow rate of the device.

if (wait_for_measurment_counter>10){

  wait_for_measurment_counter=0; 
liters_per_min_10_powerofone2 = (int)round(((number_of_spikes/(flow_counter/5000))/7.5)*10); // this math calculates the liters per minute flow rate *10^2
//  Serial.println(flow_counter); //debug code
//  Serial.println(number_of_spikes); //debug code
//  Serial.println(liters_per_min_10_powerofone2); //debug code


// reset the important values.
flow_counter=0;
number_of_spikes=1;
}
else{
wait_for_measurment_counter=wait_for_measurment_counter+1;
}
  
}


// information for serial communication
// 01 to 06 set pwm frquencies for respective pwm
// 07 sets tempaerture setpoint 1
// 08 sets temperature setpoint 2
// 09 set frequency divder one
// 10 sets frequency divder two
// the frequency is given by 2500hz/ (frequency_divider_one * freqeucny_divider_two); 



