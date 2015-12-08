# include "Hbridgepwm.h"

Hbridgepwm::Hbridgepwm (int pid_val)
{
 _pid_val = pid_val; // this line of code may be unessary.
}

void Hbridgepwm::begin() 
{ // this sets up the pwm for use (provided correct hardware of course)
  // could beef up this function to allow the input pins to be changed.
 pinMode(p1, OUTPUT); 
 pinMode(p2, OUTPUT);
 pinMode(n1, OUTPUT);
 pinMode(n2, OUTPUT);
}

void Hbridgepwm::hardwareprotect(int pid_val)
{
  _pid_val = pid_val; // so the value of the global variable is set to the local variable.
// must check if are about to switch direction.
  if (_pid_val_old >= 0)
  {
    if (_pid_val <0)
    {
     // direction has changed from forward to backwards
     
      digitalWrite(p1, LOW); // set p mosfet off to let n mosfet drain.
      delay(1*(abs(_pid_val - _pid_val_old))); // wait to let the inductive load drain, the faster motor was moving the greater amount of energy that needs to be drained.
      digitalWrite(n2, LOW);
      delay(100); // wait for the n2 fet to be fully off
      // all fets are of so it is good for set to turn them back on
    }
  }

  if (_pid_val_old <= 0)
  {
    if (_pid_val >0)
    {
     // direction has changed from backwards to forwards
      digitalWrite(p2, LOW); // set p mosfet of let n mosfet drain.
      delay(1*(abs(_pid_val_old - _pid_val))); // wait to let the inductive load drain.
      digitalWrite(n1, LOW);
      delay(100); // wait for n1 fet to be fully off.
     
    }
  }
  // finished checking for a chnage in direction, update old value.
_pid_val_old = _pid_val; 
  
}

void Hbridgepwm::set_pwm(int pid_val)
{
  _pid_val = pid_val; // here we define the constructor and seperate the public from the private variable for led.


 if (_pid_val >0)
 { 

  // forward direction pmw
  analogWrite(n2, _pid_val);
  digitalWrite(p1, HIGH);
  digitalWrite(p2, LOW);
  digitalWrite(n1, LOW);
 }
else if (_pid_val<0)
{ 
  // backwards direction
  analogWrite(n1, abs(_pid_val));
  digitalWrite(p2, HIGH);
  digitalWrite(p1, LOW);
  digitalWrite(n2, LOW);
  // n1 is pulse and p2 is kept high as the n chanell mosfets have a faster switching speed.
}
else
{ // off case
  digitalWrite(p1, LOW);
  digitalWrite(p2, LOW);
  digitalWrite(n1, LOW);
  digitalWrite(n2, LOW);
}

}


int Hbridgepwm::status(int pid_val)
{
 _pid_val = pid_val; 
if (_pid_val > 255)
{
_pid_val =255;
_ERR =1;
}
else if (_pid_val < -255)
{
 _pid_val =-255;
 _ERR=1;
}
return _ERR;
}


