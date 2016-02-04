// this will be the class that controls all of the PID1 and pwm,
// it does the PID1 by the inbuild arduion liberary and controls hard with the custom build hardware run class.
// will be a class definition currently just pseduo code.
#ifndef PID_Controll_Class_h
#define PID_Controll_Class_h
#include "PID_v1.h"
#include "SparkFun_APDS9960.h"
#include "hardware_controll_class.h"
#include <OneWire.h>
#include <DallasTemperature.h>
// Data wire is plugged into pin 2 on the Arduino
#define ONE_WIRE_BUS 41
 
static OneWire _oneWire(ONE_WIRE_BUS);
 
// Pass our oneWire reference to Dallas Temperature.
static DallasTemperature _sensors(&_oneWire);


////////////////////////////////////////////////////////////////////////////////////////////
//IMPORTANT NOTE:
//////////////////////////////////////////////////////////////////////////////////////////////

// this is the haeder of the class hbridgepwm which is used to control pwm in the code when it is given a value by PID1.
// this is the H bridge pwm set class
// it is a class that the value given by the PID1 function as the input and sets the pwm on the respective pin
// note the pin numbers in this device are hard coded not dynamically changed as should only need one or 2 h bridge in the circuit.

// to use this pwm set program
// first call begin (this sets up the function should only be called once)
// next call status to see if the hrbidfe is OK
// if it is ok call set.



class PID_Controll{
  public:
 struct PID_values_and_setpoints ValuesSetpointsStates;
    PID_Controll(int a_val);
    void begin(long unsigned int *frequency_divider_on_1, long unsigned int *frequency_divider_off_1, byte *error_vector); //will setup the PID1 objects that will be used for this class
    void update_and_Set_PID_Outputs(); // will do PID1 to find the PWM pins and update it.
    void set_LED_Flash(long unsigned int on_period_sx1000, long unsigned int off_period_sx1000); //just gives data to below class
    void set_Hardware(byte device_ID, bool discrete_action, int continuous_action);// just gives data to below class.
    void update_PID_Values(double P, double I, double D, byte ID);
    byte check_Events(void);
    void set_Event(byte,byte,unsigned int);
    
// setup the pointer to the classes
PID *PID1; // blue light
PID *PID2; // red light
PID *PID3; //pelter
Hardware_Controll *hardware_pointer;
 
// need some value to help datatpe between the PID and the luminoisty senor
uint16_t red_val_datatyper=0;
uint16_t blue_val_datatyper=0;
double blue_led_pwm = 0;
double red_led_pwm = 0;
double pelter_pwm = 0;
byte non_zero_value = 0;
byte *error_val=0;
SparkFun_APDS9960 apds = SparkFun_APDS9960();

  private:
  

};

#endif

//******************************




