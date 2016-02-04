


# include "Hardware_Controll_Class.h"



Hardware_Controll::Hardware_Controll(void)
{
  Hbridge_Hardware_Controll *hbridge_pointer = new Hbridge_Hardware_Controll();
  LED_Hardware_Controll *LED_pointer = new LED_Hardware_Controll();


}



void Hardware_Controll::begin(long unsigned int *frequency_divider_on_1, long unsigned int *frequency_divider_off_1, byte *error_vector)
{ //this setups all of the needed pins and, gives the habdles to th pointers and sets up the below classes.
   struct action_data {
      // the device ID that this class is given correspond to the indentations of these matricies.
      byte device_IDs[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};        //note wile currently a list will be turned to actual varrying numbers depending on which devices are conntected to the arduino this code works for.
      volatile byte discrete_action_pins[10] = {11, 15, 9, 3, 0, 3, 17, 31, 33, 30}; // this give the discrete action pin for the device id, note if zero means a function call is necessary to another class that deals
      // with it such as the led_controll class or the hbridge_controll_class.
      byte feed_back_pins[10] = {40, 41, 42, 43, 44, 45, 46, 47, 48, 49}; // gives the feedback pin for that device.
      bool led_controll_class_subject[10] = {0, 0, 0, 0, 1, 0, 0, 0, 0, 0}; // means will need to run the led class to implement this
      bool hbridge_controll_class_subject[10] = {0, 0, 0, 0, 0, 1, 0, 0, 0, 0}; // means will need to run the hbridge_controll_class to implement this pin

    };

    struct action_data  action_data_one;
  for (int d = 0; d <= 10; d++) { // set up the pins held as disrete action pins.
    if (action_data_one.discrete_action_pins[d] != 0)
    {
      pinMode(action_data_one.discrete_action_pins[d], OUTPUT); // set up the output pins
    }

    pinMode(action_data_one.feed_back_pins[d], INPUT); // set up the input pins
  }
  // the pointers have acces to the main class so we do not need to instanciate it.


  hbridge_pointer->begin(3, 5, 3, 4, 1, 2);
  LED_pointer->begin(frequency_divider_on_1, frequency_divider_off_1);
  Serial.print("HCB");




}

void Hardware_Controll::set_Hardware(byte device_ID, bool discrete_action, int continuous_action)
{
byte BLAH_device_id = device_ID;
byte _discrete_actionz = discrete_action;
byte _indent_j;

  // first thin must do is save these variables passed in into the private workspace.
 // _device_id = device_ID; // here we define the constructor and seperate the public from the private variable for led.
  // _discrete_action = discrete_action;
  Serial.println("RAM:");
  Serial.println(freeRam());
  _continuous_action = continuous_action;
  // next must check device ID to wheater we need to call another class or wheater this class can straight up deal with it
  // first find device_id_indent.
    struct action_data {
      // the device ID that this class is given correspond to the indentations of these matricies.
      byte device_IDs[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};        //note wile currently a list will be turned to actual varrying numbers depending on which devices are conntected to the arduino this code works for.
       byte discrete_action_pins[10] = {11, 15, 9, 3, 0, 3, 17, 31, 33, 30}; // this give the discrete action pin for the device id, note if zero means a function call is necessary to another class that deals
      // with it such as the led_controll class or the hbridge_controll_class.
      byte feed_back_pins[10] = {40, 41, 42, 43, 44, 45, 46, 47, 48, 49}; // gives the feedback pin for that device.
      bool led_controll_class_subject[10] = {0, 0, 0, 0, 1, 0, 0, 0, 0, 0}; // means will need to run the led class to implement this
      bool hbridge_controll_class_subject[10] = {0, 0, 0, 0, 0, 1, 0, 0, 0, 0}; // means will need to run the hbridge_controll_class to implement this pin

    };

    struct action_data  action_data_one;


  for (int j = 0; j < (int)8; j++)
  {

    if ((action_data_one.device_IDs[j]) == BLAH_device_id)
    {

      // have found the ID indent wanted
      _indent_j =j ;
Serial.print("success!");
Serial.print("device indent is");
Serial.println(_indent_j);
Serial.println(j);
    }
    Serial.println(action_data_one.device_IDs[j]);
  }

  // now have ID must check which class this class needs to call to implement it.
  if (action_data_one.led_controll_class_subject[_indent_j] == 1) {
    // pass the given variabls into the led controll class to deal with it.
      Serial.println("LCC");
    LED_pointer->set_Hardware(_device_id, _continuous_action);

  }
  else if (action_data_one.hbridge_controll_class_subject[_indent_j] == 1) {
    // pass the given variabls into the hbidge controll class to deal with it, // will need to go between hrbedge class if have more than one
    // do a little bit of DATATYPING!!!!!!!!!!!!!!!! before (cause dont need int anymore !!!0
      Serial.println("HBCC");
    if (_continuous_action > 0) {
      _sign = 1;
    }
    else if (_continuous_action <= 0) {
      _sign = 0;
    }
    hbridge_pointer->set_PWM((byte)_continuous_action, _sign ); // data type the int to byte so cant exceed hardware limitations.
  }
  else {
    // simple on or off of pin is required implement it below, this class can implment this it'self
    //   Serial.print("WPin"); // debug code
    //  Serial.print(action_data_one.discrete_action_pins[device_ID_indent]); //debug code
    //  Serial.print("VolLev");//debug code
    //  Serial.print(_discrete_action); //debu code



if ( _discrete_actionz==0){
  Serial.print("off");
      Serial.println("pin no is");
   Serial.println(action_data_one.discrete_action_pins[_indent_j]); 
   digitalWrite(action_data_one.discrete_action_pins[_indent_j], LOW); // implement the discrete action.
}
else if (_discrete_actionz==1){
   Serial.println("on");
      Serial.println("pin no is");
   Serial.println(action_data_one.discrete_action_pins[_indent_j]);
   digitalWrite(action_data_one.discrete_action_pins[_indent_j], HIGH); // implement the discrete action.
}
  

  }
  Serial.print("END HCCSHW");


}

void Hardware_Controll::set_LED_Flash(long unsigned int on_period_sx1000, long unsigned int off_period_sx1000) {
  // this is used to just move data from one location to another from the hardware class to the led class.

     struct action_data {
      // the device ID that this class is given correspond to the indentations of these matricies.
      byte device_IDs[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};        //note wile currently a list will be turned to actual varrying numbers depending on which devices are conntected to the arduino this code works for.
      volatile byte discrete_action_pins[10] = {11, 15, 9, 3, 0, 3, 17, 31, 33, 30}; // this give the discrete action pin for the device id, note if zero means a function call is necessary to another class that deals
      // with it such as the led_controll class or the hbridge_controll_class.
      byte feed_back_pins[10] = {40, 41, 42, 43, 44, 45, 46, 47, 48, 49}; // gives the feedback pin for that device.
      bool led_controll_class_subject[10] = {0, 0, 0, 0, 1, 0, 0, 0, 0, 0}; // means will need to run the led class to implement this
      bool hbridge_controll_class_subject[10] = {0, 0, 0, 0, 0, 1, 0, 0, 0, 0}; // means will need to run the hbridge_controll_class to implement this pin

    };

    struct action_data  action_data_one;
  Serial.println("2");
  LED_pointer->set_LED_Flash(on_period_sx1000, off_period_sx1000);
}

byte Hardware_Controll::status()
{

  *_error_value = LED_pointer->status();
  delay(10); // so the error checking interrupt can go do its things
  *_error_value = hbridge_pointer->status();
  delay(10);
}

void Hardware_Controll::check_Events(void)
{
     struct action_data {
      // the device ID that this class is given correspond to the indentations of these matricies.
      byte device_IDs[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};        //note wile currently a list will be turned to actual varrying numbers depending on which devices are conntected to the arduino this code works for.
      volatile byte discrete_action_pins[10] = {11, 15, 9, 3, 0, 7, 17, 31, 33, 30}; // this give the discrete action pin for the device id, note if zero means a function call is necessary to another class that deals
      // with it such as the led_controll class or the hbridge_controll_class.
      byte feed_back_pins[10] = {40, 41, 42, 43, 44, 45, 46, 47, 48, 49}; // gives the feedback pin for that device.
      bool led_controll_class_subject[10] = {0, 0, 0, 0, 1, 0, 0, 0, 0, 0}; // means will need to run the led class to implement this
      bool hbridge_controll_class_subject[10] = {0, 0, 0, 0, 0, 1, 0, 0, 0, 0}; // means will need to run the hbridge_controll_class to implement this pin

    };

    struct action_data  action_data_one;
  // check if an event that was told to happen has happened (i.e valve turn off) and returns the error signal one it has been feedback confirmed that that event has completed
  // if it has return correspondong error message byte

  // run through all of the elements and check if sometihng need to be check , if it is check it.
  // if the device has completed return the appropriate byte
  byte _indent = 0;
  for (byte q = 0; q <= 9; q++)
  {
    Serial.print(ValuesSetpointsStates.pending_event_device_ID[q]);
    if (ValuesSetpointsStates.pending_event_device_ID[q] != 0)
    {
       
      _indent = q;
    }
  }
Serial.println();

    switch (ValuesSetpointsStates.pending_event_type[_indent]) {
      case 0:    // want a voltage low on given pin
      Serial.print("z");
        if (analogRead(action_data_one.feed_back_pins[_device_id]) < 100)
        {
          // update the global variables table to have the modle of the current system
          noInterrupts();
          ValuesSetpointsStates.state[_indent] = 0; // save the current state of the system into the global vairabls
          interrupts();
        }
        else
        {

        }


        break;
      case 1:    //  want a voltage hi on given pin
       Serial.print("f");
        if (analogRead(action_data_one.feed_back_pins[_device_id]) > 800)
        {
          noInterrupts();
          ValuesSetpointsStates.state[_indent] = 1; // save the current state of the system into the global vairabls
          interrupts();


        }
        else
        {

        }



        break;
      case 2:    //other to be implemented later.
        /////////////////////////////////////////////////////
        ////////////////////////////////////////////////
        ////////////////////////////////////////////////////////

        break;
    }


}



void Hardware_Controll::set_Event(byte device , byte type , unsigned int end_value)
{
  // check if an event that was told to happen has happened (i.e valve turn off) and returns the error signal one it has been feedback confirmed that that event has completed
  // if it has return correspondong error message byte
  // first we must find the fist zero element that we can
  byte _indent = 0;
  for (byte s = 0; s <= 9; s++)
  {
    if (ValuesSetpointsStates.pending_event_device_ID[s] == 0)
    {
      _indent = s;
    }
    // so correctly indent with new information
  }
  if (_indent !=0){
  ValuesSetpointsStates.pending_event_device_ID[_indent] = device;
  ValuesSetpointsStates.pending_event_type[_indent] = type;
  ValuesSetpointsStates.pending_event_end_value[_indent] = end_value;
  }
  
}


