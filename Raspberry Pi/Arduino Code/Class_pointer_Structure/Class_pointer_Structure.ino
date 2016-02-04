// this is the code that runs the situation handling interrupts, the one that measures time


// the frequency controller interrupt, this interrupt is used to controllthe swicthing of the led's, occurs 3926 times a second

// the time counter / uart use interrupt. keeps track of time with resolution 123 per second updates the uart messages, runs the UART_data_COMs class that decodes them if they are completed.

// the check if time to do event OR wheater pending event has completed interrupt, runs the necessary classes once ready.

// note the timing of the counter interrupt does not need to be eaxcat of time based commands can be off by 0.1 of a second with no real problem.
// the time constraint task interrupt checks if any task in the variable_devices need to be run at the current time an runs them if they do.

//




#include "PID_Controll_Class.h"
#include "UART_data_COM.h"
//#include "Global_Varaibles.h" //debug code
byte count=0;
byte error_val = 0;

// the global measurment, setpoint and state of system structure
struct PID_values_and_setpoints ValuesSetpointsStates;

long unsigned int ocuurence_test = 0; //debug variable
int flow_occurence_test = 0; // debug debug code.
long unsigned int time_ms = 0;

// the led flicker frequency control variables.
volatile unsigned  long frequency_count = 1; // this variable is compared against the above.
unsigned  long frequency_divider_on_1 = 228;
unsigned  long  frequency_divider_off_1 = 228;
volatile unsigned  long  period_value_on = 91; // used to solve for the period (in seconds) of the high and low frequencies.
volatile unsigned  long  period_value_off = 91; // used to solve for the period (in seconds) of the high and low frequencies.
volatile bool state = 1; // used to keep track of wheater the pwm is on or off. is set to one as it set on in the setupt function.
volatile bool on_off = 0; //used to keep track of wheater the leds are on or off.

// the time_dependant action interrupt variables.
byte array_indent = 0;
struct time_check_variables { // this is an example of the strucutre used in the time check interrupt
  byte ID[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0} ; //id of device that needs to have type of action performed after set flow or time.
  short int contiion_met_action[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0,}; // the action (turn on, turn off, pwm set) that is performed after given flow or time
  long unsigned int time_of_action[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0}; // states the time at which the type of action needs to occur.
  long unsigned int required_flow_of_action[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // states the flow at which the type of action needs to occur
  bool flow_meter_ID[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // states the flow meter for which the flow needs to occurs
  byte completetion_message[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // states the message that needs to be sent to the raspberry pi upon completeion.
  // add a few more time check variabls to see if something has been completed, also need a return error message.
  byte indentor = 0;

};
// next must declare an instance of this strucutre
struct time_check_variables variable_devices;

// the UART variables.
String inputString;

// the flow meter variabls, due to the number of flow meters (11) we will need to runn a onstantly polling interrupt to find the flow rate, so will need to use another interrupt.
struct flow_sensor_variables {
  byte input_pins[6] = {10, 11, 12, 13, 14, 15};
  unsigned int toggle_counter[6] = {0, 0, 0, 0, 0, 0};
  bool previous_state[6] = {0, 0, 0, 0, 0, 0};
  long unsigned int total_flow_ml[6] = {500, 0, 0, 0, 0, 0};
  long unsigned int start_count_time[6] = {0, 0, 0, 0, 0, 0};
};
unsigned int time_between_flowcalcs = 61;

// create the flow sensor structures
struct flow_sensor_variables flow_sensor_one;

// create the necessary instances
PID_Controll PID_main(1);
UART UART_COMS(&PID_main);


void setup() {
  Serial.begin(9600);
  inputString.reserve(30);
  // put your setup code here, to run once:
  // set up the timer interrupt which will be used to keep track of fast time
  // set up the pwm pins for the 6 led's to the highest frequency (approx 31khz)
  TCCR1B = TCCR1B & 0b11111000 | 0x07; // the frequency of the timer interrupt set on overflow interrupt.
  TCCR2B = TCCR2B & 0b11111000 | 0x07; // below are the frequency of the LED's
  TCCR3B = TCCR3B & 0b11111000 | 0x05;
  TCCR4B = TCCR4B & 0b11111000 | 0x04;
  TCCR5B = TCCR5B & 0b11111000 | 0x01;
  /*
  TIMSK0 = (0 << OCIE0A) | (1 << TOIE0); // enable the timer interrupt for timer unit 1.
  TIMSK1 = _BV(TOIE1); // enable overflow as the type of interrupt used.

*/
  TIMSK2 = (0 << OCIE2A) | (1 << TOIE2); // enable the timer interrupt for timer unit 2
  TIMSK2 = _BV(TOIE2); // enable overflow as the type of interrupt used.


  TIMSK3 = (0 << OCIE3A) | (1 << TOIE3); // enable the timer interrupt for timer unit 3
  TIMSK3 = _BV(TOIE3); // enable overflow as the type of interrupt used.
/*
  TIMSK4 = (0 << OCIE4A) | (1 << TOIE4); // enable the timer interrupt for timer unit 4
  TIMSK4 = _BV(TOIE4); // enable overflow as the type of interrupt used.
*/

  // defined some analoge pins (note the locations of these pins will be changed at a later date
  pinMode(10, INPUT);
  pinMode(11, INPUT);
  pinMode(12, INPUT);
  pinMode(13, INPUT);
  pinMode(14, INPUT);
  pinMode(15, INPUT);
  // note, hardware pull down resistors are neccessary to read the output of the flow meters correctly.
  // end analgoue pin defintion.
  // this class also needs to define handle to subclasses so that it can access this data
  // begin all of the classes.
  Serial.print("ON!");
  PID_main.begin(&frequency_divider_on_1, &frequency_divider_off_1, &error_val); //begin the hardware and PID classes
  //begin the uart class.
}

void loop() {
  // put your main code here, to run repeatedly:
  // start debug code
  delay(10000);
  ocuurence_test = 0;
  flow_occurence_test = 0;
  PID_main.check_Events();

  // end debug code

  // in main loop need to continuously loop PID
  // PID_main.update_and_Set_PID_Outputs();


  //for (int p = 0; p <= 29; p++)
  // {
  //zero_Placment(ValuesSetpointsStates.device_ID[p],(unsigned int)(ValuesSetpointsStates.state[p] * 100));
  //Serial.println(ValuesSetpointsStates.device_ID[p]);
  //   }


}
/*
ISR(TIMER1_OVF_vect) { // this is the frequency pin divider interrupt, it is the fastest interrupt with an occurence rate of 3926 times per second.
  // the timing of this one is most critcal so it cannot be interrupted
  // this is the interrupt service routine function (note as an interrupt function it can only see global varables)

  if (on_off == 0) { // ignores the rest of the code if the leds are set to a permanant state via serial communication.

    if (state == 0) { // the pwm is off, next must implement frequency divider

      if (frequency_divider_off_1 > frequency_count) {
        frequency_count = frequency_count + 1; // update the count
      } else {
        // run the pwm on function, debug code
        frequency_count = 1;
        state = 1;
      }
    }

    if (state == 1) { // the pwm is on, turn it off.

      if (frequency_divider_on_1 > frequency_count) {
        frequency_count = frequency_count + 1; // update the count
      } else {
        // run the pwm off function, debug code
        frequency_count = 1;
        state = 0;
      }
    }

  }


}
*/
ISR(TIMER2_OVF_vect) { // this is time constrained procedure checking interrupt checking interrupt, occurs 30 times per second.
/*
  // checks if task need to be done now, if it does breaks to end as fast as possible, if it does not implement the task via the hardware control class.

  // this interupt must be interrupted by the two other interrupts as the latency of this interrupt is least important.
  ocuurence_test = ocuurence_test + 1; //debug code
  // we must test the time of action member of the variable devices class to see if anything needs to be acted upon.

  array_indent = 0; //reset the array indentation counter so that we can start at the beging of the array.
  // here we test the cells in the time of action array to see if any work needs to be done
  for (byte array_indent = 0; array_indent < 11; array_indent++) { // shorthand code for increase array_indent by 1 for each loop and run the for loop until array_indent =21
    if (variable_devices.time_of_action[array_indent] == 0) // no work need to be done break
    {
    }
    else  // there is a time depedant command to be done, must make sure the time is correct
    {
      if (variable_devices.time_of_action[array_indent] > time_ms) // it is not time to do the work
      {

      }
      else if (variable_devices.time_of_action[array_indent] < time_ms) // it is the correct time to do work
      {
 
          ///////// run the hardware control classs and implement the necessary hardware changes, note need to gives the function the current value of all arrays in the structure to work with.
          //variable_hardware_control(variable_devices.ID[array_indent],variable_devices.type_of_action[ID]
          // now must remove the saved action so it does not get ran again the next time this interrupt
          variable_devices.time_of_action[array_indent] = 0;
          variable_devices.ID[array_indent] = 0;
          // next we must send the signal to say that the task was completed
          variable_devices.completetion_message[array_indent] = 0;
      

        
      }
    }
  }
  // next check if any flow actions need to be performed.
  for (byte array_indent = 0; array_indent < 11; array_indent++) { // shorthand code for increase array_indent by 1 for each loop and run the for loop until array_indent =21
    if (variable_devices.required_flow_of_action[array_indent] == 0) // no work need to be done break
    {

    }
    else  // there is a time depedant command to be done, must make sure the time is correct
    {

      if (variable_devices.required_flow_of_action[array_indent] > flow_sensor_one.total_flow_ml[variable_devices.flow_meter_ID[array_indent]] ) // it is not time to do the work
      {

      }
      else if (variable_devices.time_of_action[array_indent] < flow_sensor_one.total_flow_ml[variable_devices.flow_meter_ID[array_indent]]) // it is the correct time to do work
      {
     //   Serial.println("dummymadeit"); //debug code

        ///////// run the hardware control classs and implement the necessary hardware changes, note need to gives the function the current value of all arrays in the structure to work with.
        //variable_hardware_control(variable_devices.ID[array_indent],variable_devices.type_of_action[ID]
        PID_main.set_Hardware(variable_devices.ID[array_indent], (bool)variable_devices.contiion_met_action[array_indent] , variable_devices.contiion_met_action[array_indent]);
        // now must remove the saved action so it does not get ran again the next time this interrupt
      
        variable_devices.required_flow_of_action[array_indent] = 0;
        variable_devices.ID[array_indent] = 0;
        // next we must send the signal to say that the task was completed
        variable_devices.completetion_message[array_indent] = 0;
      

      }
    }
  }
  */
  // next ceck if any pending events have concluded.


  // only need to do the below about 5 times a second, 30 is too many so will just skip over this when not wanted.
  count = count+1;
  if (count ==30)
  {
  count =0; 
  


  }
  
}

ISR(TIMER3_OVF_vect) { // this is time counting interrupt, goes off 60 times per second.
 
  if (time_ms != 4294967295) {
    time_ms = time_ms + 1;

    //this counter value keeps track of time with a resolution of 122 per second, thus a value increase of 122 mean one second has passed.
  }
  else {
    time_ms = 0; // will not be usign timer overflow, just reseter all values when is high and notihng is waiting to be done. (this way use less of the very contrained fram)
  }
  // will also use this timer to update serial communication as fast as possible
  // next check and grow on serial.


  while (Serial.available()) {

    // get the new byte:
    char inChar = (char)Serial.read();

    // add it to the inputString:
    if (inputString.length() == 30) {
      // have bad data, reset string and flush
      Serial.flush();
      inputString = "";
    } else {
     
      inputString += inChar;

      // if the incoming character is a newline, set a flag
      // so the main loop can do something about it:
      if (inChar == 10) { // this states the type of trailing null used.
        // we have a complete message, need to do some work with this message.
        // run the work on message class uart_acton_(inputstrong) // NOTE MUST PASS THE VARAIABLE NOT THE POINTER or the string will be altered when it is beign read.
        UART_COMS.decode_Message(inputString);
        inputString = ""; // as we have sent the data away and need to reset it.

      }
    }




  }


}
/*
ISR(TIMER4_OVF_vect) { // this is the interrupt that checks wheater the digital pin pulse is high or low against previous to note the flow rate and undate related values.
  flow_occurence_test = flow_occurence_test + 1; // debug debug code.

  // first need to count how many pulses have occured from that flow meter.
  // note the flow meter counters will not not overflows as they will be reset by uart. commands
  // first thing to do is poll the value of the pin to find out wheater the pin is high or low so we can know if a change has occured,this will be stored in toggle.
  // note this inteerupt cannt staright up calculate flow rates as a number of pulse over time of a second or so is reqiured to give the flow rate and thus the total flow.

  for (int w = 0; w < 7; w++) {
    if (digitalRead(flow_sensor_one.input_pins[w]) != flow_sensor_one.previous_state[w]) {
      // a change has occured.

      flow_sensor_one.previous_state[w] = !(flow_sensor_one.previous_state[w]); // toggle it to the next state
      flow_sensor_one.toggle_counter[w] = flow_sensor_one.toggle_counter[w] + 1; // update the number of spikes seen.
    }
  }
  //start debug code


  //end debug code



  // this counts the number of spikes that occurs. the time_of_start _count must be updated by the uart function when we wish to start count. next we must check wheater enough time has
  // passes for us to take data to approximate the given flow rate and the totoal flow.
  // repeate the above code for each wanted flow sensor.
  // check wheater we need to take measurments.

  // means we care about the flow rate.
  if (time_between_flowcalcs < time_ms) { // then ready to calculate new flow rates and update total flow values.


    if (time_between_flowcalcs < 4294967256) {
      time_between_flowcalcs = time_between_flowcalcs + 61;
    }

    else {
      time_between_flowcalcs = 1  ;
    }
    // the above code simply prevents overflows.


    // calculate current flow rate for the device (need to know the device before this can be done
    // i.e flowrate = 1.2*toggle number (ml)
    // calculate total flow
    // i.e total flow = total_flow * 40/123 *flow rate


    // update global flow count variable strucutre that uart and the event handling code both have access to.
    // struct stc = total flow


    //reset counter variabls.
    //flow_sensor_one.toggle_counter=0;




  }

}


*/

///////////////////////////
/////////
//
// TO DO PENDING EVENT IN HARDWARE CONTROLLS SO DO NOT SEND BACK TO PIE ONCE AN EVENT HAS ATUALY COMPLETED.
int freeRam() 
{
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}


