
 #include "PID_Controll_Class.h"


PID_Controll::PID_Controll(int a_val)
{
PID *PID1 = new PID();
PID *PID2 = new PID();
PID *PID3 = new PID();
Hardware_Controll *hardware_pointer = new Hardware_Controll();



}


void PID_Controll::begin(long unsigned int *frequency_divider_on_1, long unsigned int *frequency_divider_off_1, byte *error_val)
{ // this sets up all of the PID objects that will be used in this code
  //intialise the PID instances
  PID1->begin(&ValuesSetpointsStates.blue_luminosity_value, &blue_led_pwm, &ValuesSetpointsStates.blue_luminosity_setpoint,ValuesSetpointsStates.Kp_blue_led , ValuesSetpointsStates.Ki_blue_led, ValuesSetpointsStates.Kd_blue_led, DIRECT);
  PID2->begin(&ValuesSetpointsStates.red_luminosity_value, &red_led_pwm, &ValuesSetpointsStates.red_luminosity_setpoint, ValuesSetpointsStates.Kp_red_led, ValuesSetpointsStates.Ki_red_led, ValuesSetpointsStates.Kd_red_led, DIRECT);
  PID3->begin(&ValuesSetpointsStates.average_temperature, &pelter_pwm, &ValuesSetpointsStates.average_temperature_setpoint, ValuesSetpointsStates.Kp_pelter_one, ValuesSetpointsStates.Ki_pelter_one, ValuesSetpointsStates.Kd_pelter_one, DIRECT);

  // set the limits for these values.
  PID1->SetOutputLimits(0, 255);
  PID2->SetOutputLimits(0, 255);
  PID3->SetOutputLimits(-255, 255);

  // set the mode to automatic as there is realy no other opion (means code only generates new outputs when thinks they are needed)
 PID1->SetMode(AUTOMATIC);
 PID2->SetMode(AUTOMATIC);
 PID3->SetMode(AUTOMATIC);

  // set the controller directions
  PID1->SetControllerDirection(DIRECT);
  PID2->SetControllerDirection(DIRECT);
  PID3->SetControllerDirection(DIRECT);

  //next set up the child instances of the hardware controll class
hardware_pointer->begin(frequency_divider_on_1, frequency_divider_off_1, error_val);

  // next we need to begin the onewire hardware
  _sensors.begin();

  // next we will begin the i2c hardware.
  apds.init();
  apds.enableLightSensor(false);

}

void PID_Controll::update_and_Set_PID_Outputs()
{
  // this will be a very large class with a number of steps.
  
  //first talk to all measuring devices to uodates all values

    //get the temp value from the one wire class
    // note since temp readin is slow in one_wire_talk it will check if enoguht time has calibrated for the sensors to be ready to give new data before requsting it and stroing it.
    // else this functions will continues to run on old data (which is fine).
   _sensors.requestTemperatures(); //request new temparature values
    ValuesSetpointsStates.temperature_values[0]=_sensors.getTempCByIndex(0);
    ValuesSetpointsStates.temperature_values[1]=_sensors.getTempCByIndex(1);
    ValuesSetpointsStates.temperature_values[2]=_sensors.getTempCByIndex(2);
    ValuesSetpointsStates.temperature_values[3]=_sensors.getTempCByIndex(3);
    ValuesSetpointsStates.temperature_values[4]=_sensors.getTempCByIndex(4);
    ValuesSetpointsStates.temperature_values[5]=_sensors.getTempCByIndex(5);
    // find the average temperature and update it.

    // need to make a small for loop here that finds the average and removes any values which are not realistic temperature values.
    // reset the holding values
    noInterrupts(); // must prevent the UART interrupt from occuring here as we are updating important data that will be sent over uart.
    ValuesSetpointsStates.average_temperature=0;
    non_zero_value=0;
    for (int i=0; i <= 6; i++){
    if (ValuesSetpointsStates.temperature_values[i]<70 && ValuesSetpointsStates.temperature_values[i] >1){
     ValuesSetpointsStates.average_temperature = ValuesSetpointsStates.average_temperature+ValuesSetpointsStates.temperature_values[i];
     non_zero_value = non_zero_value+1;
    }
     }
    ValuesSetpointsStates.average_temperature = ValuesSetpointsStates.average_temperature/non_zero_value ;
    // update the average temperature.
    interrupts(); // the data is updated UART protocol is now clear to send if need be.


    // get the luminsoity vaues from the i2c class.
    // i2c_class(ID value, &luminosity strucutre); // will talk to the light sensor via i2C, will send get new data request the not read untill enoguth time has past much similar to the
    // i2c class.


    !apds.readRedLight(red_val_datatyper);
    ValuesSetpointsStates.red_luminosity_value = (double)red_val_datatyper;
    !apds.readBlueLight(blue_val_datatyper);
    ValuesSetpointsStates.blue_luminosity_value = (double)blue_val_datatyper;
   



    // next update the global variables in the structure passed to this class upon intialisation
    // this is done by handing the structure to the other classes and they save the data in it.

    // next do PID on these setpoints to get the appropiate pwms.
   PID1->Compute();
   PID2->Compute();
   PID3->Compute();
    // this functions automatically finds the PID value and saves it in the above varaible whose pointers are given upon intilsation.


    // next implement the pwms variables that are given as output from the PID function
    hardware_pointer->set_Hardware(5,1,blue_led_pwm);
    hardware_pointer->set_Hardware(6,1,red_led_pwm);
    hardware_pointer->set_Hardware(7,1,pelter_pwm);
   ////////////////////
   //must update the variable ID value as the iD table has not yet been completed.
   ////////////////////

   // next must make sure everythin is in the off mode, will write a function to do this when the hardware is known.


  
}
void PID_Controll::set_LED_Flash(long unsigned int on_period_sx1000, long unsigned int off_period_sx1000)
{
  // just pass these variabls down the line
  Serial.println("1");
  hardware_pointer->set_LED_Flash(on_period_sx1000, off_period_sx1000);
}

void PID_Controll::set_Hardware(byte device_ID, bool discrete_action, int continuous_action)
{
  // just pass these variabls down the line
 hardware_pointer->set_Hardware(device_ID, discrete_action, continuous_action);
}

void PID_Controll::update_PID_Values(double P, double I, double D, byte ID)
{
  // simply need to update these values to the correct PID.
  switch (ID) {



    
    case 1:
      //case on is change the pelter turnings
      ValuesSetpointsStates.Kp_pelter_one=P;
 ValuesSetpointsStates.Kp_pelter_one=I;
 ValuesSetpointsStates.Kp_pelter_one=D;
      
    PID3->SetTunings(ValuesSetpointsStates.Kp_pelter_one, ValuesSetpointsStates.Ki_pelter_one, ValuesSetpointsStates.Kd_pelter_one);

    
      break;
    case 2:
      //case 2 is change the led turnings
      ValuesSetpointsStates.Kp_blue_led =P;
      ValuesSetpointsStates.Ki_blue_led = I;
      ValuesSetpointsStates.Kd_blue_led = D;
      ValuesSetpointsStates.Kp_red_led =P;
      ValuesSetpointsStates.Ki_red_led = I;
      ValuesSetpointsStates.Kd_red_led = D;
      


      
   PID2->SetTunings(ValuesSetpointsStates.Kp_blue_led, ValuesSetpointsStates.Ki_blue_led, ValuesSetpointsStates.Kd_blue_led);
    PID1->SetTunings(ValuesSetpointsStates.Kp_red_led, ValuesSetpointsStates.Ki_red_led, ValuesSetpointsStates.Kd_red_led);



    
      break;

    default:
      break;
  }


}
 byte PID_Controll::check_Events()
 {
  
 // pass info down the line to the hardware controll class and pass the reults back
 hardware_pointer->check_Events();
 
 }

 void PID_Controll::set_Event(byte device ,byte type ,unsigned int end_value)
 {
  hardware_pointer->set_Event(device ,type ,end_value);
  
 }



