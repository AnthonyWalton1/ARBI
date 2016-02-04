

#ifndef Hbridge_Hardware_Controll_Class_h
#define Hbridge_Hardware_Controll_Class_h
#include "Arduino.h"



class Hbridge_Hardware_Controll {
  public:
    Hbridge_Hardware_Controll(void);
    void begin(byte pwm, byte IN_f, byte IN_b, byte CS , byte DIAGa, byte DIAGb); // will set up the pwm pins for use (done this way as mutiple hbrides may be in use in this system
    void set_PWM(byte pid_val, bool direction); // will set the correct pwm on the correct pin if the error check return negative.
    byte status();
    byte  _ERR=0;
  private:
    byte _pid_val = 5;
    bool _direction = 0;

    // the new h bridge component reuires different pinout
    byte _pwm_pin = 0; // pwm pin for the hbridge
    byte _IN_f = 0; // forward on pin
    byte _IN_b = 0; //backwards on pin
    byte _CS = 0; // current sense pin
    byte _DIAGa = 0; //error check pin 1
    byte _DIAGb = 0; // error check pin 2
};

#endif

//*********************************************************************************************************************************

