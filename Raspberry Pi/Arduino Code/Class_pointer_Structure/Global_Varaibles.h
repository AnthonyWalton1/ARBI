// this struct will be a global structure which respective classes update for uart.
#ifndef Global_Varaibles_h
#define Global_Varaibles_h

struct PID_values_and_setpoints {
  double blue_luminosity_value = 0;
  double blue_luminosity_setpoint = 0;
  double red_luminosity_value = 0;
  double red_luminosity_setpoint = 0;
  double average_temperature_setpoint = 25;
  double temperature_values[6] = {25, 25, 25, 25, 25, 25};
 double average_temperature = 0;
  double Kp_blue_led = 100, Ki_blue_led = 0.8, Kd_blue_led = 0.01;
  double Kp_red_led = 100, Ki_red_led = 0.8, Kd_red_led = 0.01;
 double Kp_pelter_one = 100, Ki_pelter_one = 0.8, Kd_pelter_one = 0.01;
  volatile byte Systemdevice_ID[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
  volatile byte state[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  volatile bool error_vector[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
volatile byte pending_event_device_ID[10] = {1, 7, 6, 6, 6, 5, 5, 3, 4, 1}; // give the ID of device which acion is begin waited to be comleted (i.e turn on / turn off)
  volatile  byte pending_event_type[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // gives the tye of event , currently is just on(1), off(0)
   volatile byte pending_event_end_value[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // gives the value that is wanted, i.e High, 0 = LOW
};

extern struct PID_values_and_setpoints ValuesSetpointsStates;
#endif
