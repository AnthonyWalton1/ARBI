// this will be the class that takes the uart values and implement what it means
// this has four main steps toit
// first check if string is of correct format. if it is decide which type of data packet it is
#ifndef UART_data_COM_h
#define UART_data_COM_h
#include "PID_Controll_Class.h"


class UART {
  public:
    struct PID_values_and_setpoints ValuesSetpointsStates;
    UART(PID_Controll *PID_in); // upon intialization we will need to give this class a hadle
    void begin(void); // will set up all the pins used in the hardware, will also setup the hbridge controll class.
    void decode_Message(String); // will get the correct message type and act accordingly
    void send_Setpoints(void); // these two functions will simply send setpoint data.
    void send_Measurments(void);
    void send_System_State(void); // sends the state of the whole system in variables
    void zero_Placment(unsigned long int, unsigned long int);
    void variable_Update(void); // moved the variable update switch stament here to neaten the code for type 1 data packet
    void device_set(byte,byte); // move the device  update switch stament here to neater code for type 2 data packets.
    void dependant_action_set(void); // move the depeandant action switch stament here to neaten code for type 3 data packets
    void bounce_back(String, bool); // returns the given message with an additional error code
    private:

    unsigned int dummy_value; // dummy value
    String _inputstring;
    byte variable_ID = 0;
    double value = 0;
    // type one message above
    byte device_ID = 0;
    bool state = 0; // used for wheater on (open) or off (closed) is wanted.
    // type two message above
    byte device_ID_measure = 0;
    byte device_ID_controll = 0;
    byte action_type = 0;
    unsigned int amount_of_type = 0;
    byte secondary_action = 0;
    // type three message above
    // the below value are used to indent the string to make the code simpler
    byte v1 = 0;
    byte v2 = 0;
    byte v3 = 0;
    byte v4 = 0;
    byte v5 = 0;
    byte v6 = 0;
    byte v7 = 0;
    byte _digits = 0;
    bool _type = 0;
    bool _valid=0;
    // we will need a pointer to the pre eisting PID_controll class so that this class can access that classes methods whilsr main can aslo access that classes methods.
    PID_Controll *PID_main_instance; // the handle to the structure.

    // must add the hbbridge_controll_class as a private class that this class can access.
    // must add the led controll class as a private class that this class can access.

};

#endif


