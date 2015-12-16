// this is the haeder of the class hbridgepwm which is used to control pwm in the code when it is given a value by pid.
// this is the H bridge pwm set class
// it is a class that the value given by the pid function as the input and sets the pwm on the respective pin
// note the pin numbers in this device are hard coded not dynamically changed as should only need one or 2 h bridge in the circuit.

// to use this pwm set program
// first call begin (this sets up the function should only be called once)
// next call status to see if the hrbidfe is OK
// if it is ok call set.

#ifndef hbridgepwm_h
#define hbridgepwm_h
#include"Arduino.h"  
// #include"hbridgepwm.cpp"


class Hbridgepwm {
public:
Hbridgepwm(int pid_val);
int begin(int pwm,int IN_f,int IN_b, int CS , int DIAGa, int DIAGb); // will set up the pwm pins for use
void set_pwm(int pid_val); // will set the correct pwm on the correct pin
int status(int pid_val); // will return 0 for good, 1 for pid value 2 high and 3 for the hbridge has developed a fault
int current(); // will return the value of the curent

private:
int _pid_val=5;
int _pid_val_old=5;
int _ERR=0;
// the new h bridge component reuires different pinout
int _pwm=0; // pwm pin for the hbridge
int _IN_f=0; // forward on pin
int _IN_b=0; //backwards on pin
int _CS =0; // current sense pin
int _DIAGa =0; //error check pin 1
int _DIAGb = 0; // error check pin 2
int _voltage_value=0; // holds the current that is being sunk through the hbridge.
};

#endif

//*********************************************************************************************************************************

