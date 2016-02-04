
# include "LED_Hardware_Controll_Class.h"

LED_Hardware_Controll::LED_Hardware_Controll(void)
{
}

// change, begin function now updates the pin names so we can have mutiple classes and can adjust the pins that each class uses.

void LED_Hardware_Controll::begin(long unsigned int *frequency_divider_on_1, long unsigned int *frequency_divider_off_1)
{ // this setups all of the pins that we need with anypullup or pull downs necessary.
  // only got two output pins, one for blue and one for red
  //note actual location of pin is set to chanhe
  pinMode(10 , OUTPUT); //red led matrix control
  pinMode(11 , OUTPUT); // blue led matrix control
  // need to save these addresses into the pointers
  pointer_to_frequency_divider_on_1 = frequency_divider_on_1;
  pointer_to_frequency_divider_off_1 = frequency_divider_off_1;
  Serial.print("BEGIN LC");
}

void LED_Hardware_Controll::set_Hardware(byte device_ID, byte continuous_action)
{
  // note outpin may/will need to be changed.
  _pwm_value = continuous_action;
  _device_ID = device_ID;
  Serial.print("LSHW"); //debug code

  if (device_ID == 26) {   //device ID of red light matirx
    analogWrite(10, _pwm_value); // set the lumiosity based on the PWM value
  }
  else if (device_ID = 27) { //device ID of the blue light matrx
    analogWrite(10, _pwm_value); // set the luminosity based on the PWM value
  }


}

void LED_Hardware_Controll::set_LED_Flash(long unsigned int on_period_sx1000, long unsigned int off_period_sx1000)
{
  Serial.println("SFLAS"); //debug code
  noInterrupts();
  *pointer_to_frequency_divider_on_1 = (int)(on_period_sx1000 * 3.926);
  *pointer_to_frequency_divider_off_1 = (int)(off_period_sx1000 * 3.926);
  interrupts(); // must disable interrupts while we fiddle with thier variabls.
}

byte LED_Hardware_Controll::status() {
  // will check hardware to see if functional, currently not implemented as hardware this class talks to is not known.
  _err = 0;



}

