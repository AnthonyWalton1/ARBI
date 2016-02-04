

#ifndef Hardware_Controll_Class_h
#define Hardware_Controll_Class_h
#include "LED_Hardware_Controll_Class.h"
#include "Hbridge_Hardware_Controll_Class.h"
#include "Global_Varaibles.h"
// #include "Arduino.h"



class Hardware_Controll {
  public:
    struct PID_values_and_setpoints ValuesSetpointsStates;
    Hardware_Controll(void);
    void begin(long unsigned int *frequency_divider_on_1, long unsigned int *frequency_divider_off_1, byte *error_vector); // will set up all the pins used in the hardware, will also setup the hbridge controll class.
    void set_Hardware(byte device_ID, bool discrete_action, int continuous_action); // will set the correct pin with on or off or a pwm value
    void set_LED_Flash(long unsigned int on_period_sx1000, long unsigned int off_period_sx1000);
    void check_Events(void); // checks the vectors of pending events and sees if any have been completed it they have the arduino global variables of the system state are updates
    void set_Event(byte, byte, unsigned int); // sets the pedning events vectors with pending event right before the hardware begins to iplemetn it.

    byte status();

    // will need a new function
  private:
    byte _device_id;
    bool _discrete_action;
    int _continuous_action = 0;
    byte device_ID_indent = 0;
    bool _sign = 0;
    byte*_error_value;

    int freeRam()
    {
      extern int __heap_start, *__brkval;
      int v;
      return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
    }

    /////////////////////////////////////////////////////////////////////////////// figure out how pendign event will work

    //////////////////////////////////////////////////////////////////////////////// figure out how pending event will work
    // need vairables for pointers to all of the classes this class needs to talk to
    Hbridge_Hardware_Controll *hbridge_pointer;
    LED_Hardware_Controll *LED_pointer;

    // must have a private object of the led_hardware_controll_class.
    // create the pointers to the LED and HBrdge class





};

#endif

