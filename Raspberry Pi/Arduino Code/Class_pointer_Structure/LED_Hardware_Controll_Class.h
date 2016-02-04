

#ifndef LED_Hardware_Controll_Class_h
#define LED_Hardware_Controll_Class_h
#include "Arduino.h"

class LED_Hardware_Controll {
  public:
    LED_Hardware_Controll(void); // upon intialization we will need to give this class a hadle
    void begin(long unsigned int *frequency_divider_on_1, long unsigned int *frequency_divider_off_1); // will set up all the pins used in the hardware, will also setup the hbridge controll class.
    void set_Hardware(byte device_ID, byte continuous_action); // will set the correct pin with the correct analogue pwm.
    void set_LED_Flash(long unsigned int on_period_sx1000, long unsigned int off_period_sx1000);
    byte status();
  private:
    byte _pwm_value = 0;
    byte _device_ID = 0;
    byte _err = 0;
    unsigned long int *pointer_to_frequency_divider_on_1;
    unsigned long int *pointer_to_frequency_divider_off_1;

};

#endif

