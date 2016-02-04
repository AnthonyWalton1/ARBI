


# include "Hbridge_Hardware_Controll_Class.h"

Hbridge_Hardware_Controll ::Hbridge_Hardware_Controll(void)
{

}


// change, begin function now updates the pin names so we can have mutiple classes and can adjust the pins that each class uses.

void Hbridge_Hardware_Controll::begin(byte pwm_pin, byte IN_f, byte IN_b, byte CS , byte DIAGa, byte DIAGb)
{ // this sets up the pwm for use (provided correct hardware of course)
  // could beef up this function to allow the input pins to be changed.
  _pwm_pin = pwm_pin;
  _IN_f = IN_f;
  _IN_b = IN_b; // udate the local variables with the given ones.
  _CS = CS;
  _DIAGa = DIAGa; //error check pin 1
  _DIAGb = DIAGb; // error check pin 2
  pinMode(_pwm_pin, OUTPUT);
  pinMode(_IN_f, OUTPUT);
  pinMode(_IN_b, OUTPUT);
  pinMode(CS, INPUT);
  pinMode(_DIAGa, OUTPUT);
  digitalWrite(_DIAGa, HIGH);
  pinMode(_DIAGb, INPUT);
  Serial.print("BHB ");
}

void Hbridge_Hardware_Controll::set_PWM(byte pid_val, bool direction)
{
  _pid_val = pid_val; // here we define the constructor and seperate the public from the private variable for led.
  // this is a resitive load so we do not need to care about fast changes
  _direction = direction;

  Serial.print("HBHCSPWM");

  if (( digitalRead(_DIAGb) == HIGH)) // then the hbridge has pulled the pin high to signifi it is operating functionaly.
  {

    if (_direction == 1)
    {

      // forward direction pmw
      analogWrite(_pwm_pin, _pid_val);
      digitalWrite(_IN_f, HIGH);
      digitalWrite(_IN_b, LOW);
    }
    else if (_direction == 0)
    {
      // backwards direction
      analogWrite(_pwm_pin, abs(_pid_val));
      digitalWrite(_IN_b, HIGH);
      digitalWrite(_IN_f, LOW);
      // n1 is pulse and p2 is kept high as the n chanell mosfets have a faster switching speed.
    }


  }
}


byte Hbridge_Hardware_Controll::status()
{
  _ERR = 0;
  // next check to see if Hbridge is opeational
  if (( digitalRead(_DIAGb) == LOW)) // then the hbridge has pulled low to signifi a problem
  {
    _ERR = 1;
  }

  if ( 10.2 * analogRead(_CS)  > 40000) // means current is exceeding expected operational capacity, note will need to be adjusted later on.
  { // read volatge on current sensing pin of the hbridge
    _ERR = 2;
  }

  return _ERR ;
}



