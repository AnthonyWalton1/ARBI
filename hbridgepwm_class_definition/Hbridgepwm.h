// this is the haeder of the class hbridgepwm which is used to control pwm in the code when it is given a value by pid.
// this is the H bridge pwm set class
// it is a class that the value given by the pid function as the input and sets the pwm on the respective pin
// note the pin numbers in this device are hard coded not dynamically changed as should only need one or 2 h bridge in the circuit.

// to use this pwm set program
// first call begin (this sets up the function should only be called once)
// next call hardware protect once we have a pid value
// then call status
// then call set, if status was OK



#ifndef hbridgepwm_h
#define hbridgepwm_h
#include"Arduino.h"  



class Hbridgepwm {
public:
Hbridgepwm(int pid_val);
void begin(); // will set up the pwm pins for use
void set_pwm(int pid_val); // will set the correct pwm on the correct pin
void hardwareprotect(int pid_val); // checks if a directional switch is about to occur and lets the inductor drain to prevent curernt spike. It also prevents temproary shorts de to swithcing speeds of the mosfets
int status(int pid_val); // will return 0 for good or 1 for pid_val was not valid.

private:
int _pid_val=5;
int _pid_val_old=5;
int _ERR=0;
// the new h bridge component reuires different pinout
int pwm=9;
int IN_f=10;
int IN_b=11;
};

#endif

//*********************************************************************************************************************************

