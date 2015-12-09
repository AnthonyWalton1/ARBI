  
// #include"hbridgepwm.cpp"

# include "Hbridgepwm.h"

Hbridgepwm::Hbridgepwm (int pid_val)
{
 _pid_val = pid_val; // this line of code may be unessary.
}


// change, begin function now updates the pin names so we can have mutiple classes and can adjust the pins that each class uses.
 
int Hbridgepwm::begin(int pwm,int IN_f,int IN_b, int CS , int DIAGa, int DIAGb) 
{ // this sets up the pwm for use (provided correct hardware of course)
  // could beef up this function to allow the input pins to be changed.
_pwm= pwm;
_IN_f= IN_f;
_IN_b= IN_b; // udate the local variables with the given ones.
_CS =CS;
_DIAGa =DIAGa; //error check pin 1
_DIAGb = DIAGb; // error check pin 2
 pinMode(_pwm, OUTPUT);
 pinMode(_IN_f, OUTPUT);
 pinMode(_IN_b, OUTPUT);
 pinMode(CS, INPUT);
 pinMode(_DIAGa, OUTPUT);
 digitalWrite(_DIAGa, HIGH);
 pinMode(_DIAGb, INPUT);
}

void Hbridgepwm::set_pwm(int pid_val)
{
  _pid_val = pid_val; // here we define the constructor and seperate the public from the private variable for led.


 if (_pid_val >0)
 { 

  // forward direction pmw
  analogWrite(_pwm, _pid_val);
  digitalWrite(_IN_f, HIGH);
  digitalWrite(_IN_b, LOW);
 }
else if (_pid_val<0)
{ 
  // backwards direction
  analogWrite(_pwm, abs(_pid_val));
  digitalWrite(_IN_b, HIGH);
  digitalWrite(_IN_f, LOW);
  // n1 is pulse and p2 is kept high as the n chanell mosfets have a faster switching speed.
}
else
{ // off case
  digitalWrite(_pwm, LOW);
  digitalWrite(_IN_f, LOW);
  digitalWrite(_IN_b, LOW);
}

}


int Hbridgepwm::status(int pid_val)
{
_ERR =0; 
 // first chech to see if were given valid pid value
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

// next check to see if Hbridge is opeational
if (( digitalRead(_DIAGb) == LOW)) // then the hbridge has pulled low to signifi a problem
{
_ERR = 2;
}

return _ERR ;
}

int Hbridgepwm::current()
{
_voltage_value = 10.2*analogRead(_CS); // reads the volatge at the current sense pin to determine the current that is flowing through the h bridge.
return _voltage_value;
}


