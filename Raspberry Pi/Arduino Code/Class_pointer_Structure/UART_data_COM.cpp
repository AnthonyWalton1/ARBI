# include "UART_data_COM.h"


UART::UART(PID_Controll *PID_handle_in)
{
  _inputstring.reserve(30);
  // setup the handle to the PID class.
  PID_main_instance = PID_handle_in;


}

void  UART::begin() // upon intialisation must get an array of pointers or global variable to the conditional activoties
{
  // this class has no intialisation requirments.
  _digits = 1;
  PID_main_instance->check_Events() ; //debug code to see if this works

}

void  UART::decode_Message(String _inputstring)
{
  // first must check if message is off correct length for one of the three types
  _inputstring.trim(); // remove the carrage return
  _inputstring.trim(); // remove the new line
  //check the length.
  if (_inputstring.length() == 11)
  { // type 1 message
    if ((_inputstring[3] == 95) )
    {
      Serial.print("UDM:");// debug code
      // data in is probably good so begin to decode it and place it into variabls
      v1 = _inputstring[0] - 48;
      v2 = _inputstring[1] - 48;
      v3 = _inputstring[2] - 48;
      variable_ID = (v1) * 100 + (v2) * 10 + (v3) * 1;

      v1 = _inputstring[4] - 48;
      v2 = _inputstring[5] - 48;
      v3 = _inputstring[6] - 48;
      v4 = _inputstring[7] - 48;
      v5 = _inputstring[8] - 48;
      v6 = _inputstring[9] - 48;
      v7 = _inputstring[10] - 48;
      value = ((v1) * 10000 + (v2) * 1000 + (v3) * 100 + (v4) * 10 + (v5) * 1 + (v6) * 0.1 + (v7) * 0.01) ;

      ///////////////////////////////////////////////////////////
      UART::bounce_back(_inputstring,0);
      /////////////////////////////////////////////////////////
      UART::variable_Update();
      //////////////////////////////////////////////////////////

    }
    else
    {
      // data in was bad.
      ///////////////////////////////////////////////////////////
      UART::bounce_back(_inputstring,1);
      /////////////////////////////////////////////////////////


    }


  }
  else if (_inputstring.length() == 5)
  { // type 2 message
    // data in is probably good so begin to decode it and place it into variabls

    if ((_inputstring[3] == 95) )
    {
      v1 = _inputstring[0] - 48;
      v2 = _inputstring[1] - 48;
      v3 = _inputstring[2] - 48;
      device_ID = (v1) * 100 + (v2) * 10 + (v3) * 1;

      v1 = _inputstring[4] - 48;
      state = ((v1)) ;
    

      ///////////////////////////////////////////////////////////
      UART::bounce_back(_inputstring,0);
      /////////////////////////////////////////
     UART::device_set((byte)device_ID,(byte)state); // run the device setmethod to set the correct device to on or off.
      /////////////////////////////////////
    }
    else
    {
      ///////////////////////////////////////////////////////////
      // should check error vector here.
      UART::bounce_back(_inputstring,1);
      /////////////////////////////////////////

    }


  }
  else if (_inputstring.length() == 15)
  { // type 3 message


    if ((_inputstring[3] == 95) && (_inputstring[7] == 95) && (_inputstring[9] == 95) && (_inputstring[13] == 95) )
    {
      v1 = _inputstring[0] - 48;
      v2 = _inputstring[1] - 48;
      v3 = _inputstring[2] - 48;
      device_ID_measure = (v1) * 100 + (v2) * 10 + (v3) * 1;

      v1 = _inputstring[4] - 48;
      v2 = _inputstring[5] - 48;
      v3 = _inputstring[6] - 48;
      device_ID_controll = (v1) * 100 + (v2) * 10 + (v3) * 1;

      v1 = _inputstring[8] - 48;
      action_type = v1;

      v1 = _inputstring[10] - 48;
      v2 = _inputstring[11] - 48;
      v3 = _inputstring[12] - 48;
      amount_of_type = (v1) * 100 + (v2) * 10 + (v3) * 1;

      v1 = _inputstring[14] - 48;
      secondary_action = v1;



      ///////////////////////////////////////////////////////////
      UART::bounce_back(_inputstring,0);
      /////////////////////////////////////////
      // need to update vairbals in main so that the interrupt can update these variabls
      /////////////////////////////////////////////
      //update varibale function or just update the global variable.
      /////////////////////////////////////////////
    }
    else
    {
      //data was bad.

      ///////////////////////////////////////////////////////////
      UART::bounce_back(_inputstring,1);
      /////////////////////////////////////////

    }

  }

  else if (_inputstring.length() == 4)
  {

    v1 = _inputstring[0] - 48;
    v2 = _inputstring[1] - 48;
    v3 = _inputstring[2] - 48;
    v4 = _inputstring[3] - 48;

    value = ((v1) * 1000 + (v2) * 100 + (v3) * 10 + (v4) * 1 );

    if (value == 9999)
    {
      // this is the special case that the setpoints need to be send
      UART::bounce_back(_inputstring,0);
      UART::send_Setpoints();
    }
    else if (value == 8888)
    {
      // this is the special case that the measurments need to be send
      UART::bounce_back(_inputstring,0);
      UART::send_Measurments();

    }
    else if (value == 7777)
    {
      // this is the special case that the measurments need to be send
      UART::bounce_back(_inputstring,0);
      UART::send_System_State();
    }
  else
  {
      ///////////////////////////////////////////////////////////
      UART::bounce_back(_inputstring,1);
      ////////////////////////////////////////
  }


  }
  else
  {
      ///////////////////////////////////////////////////////////
      UART::bounce_back(_inputstring,1);
      ////////////////////////////////////////
  }





}


void UART::send_Setpoints(void)
{
  // send all the setpoitn data
  zero_Placment(15, (long unsigned int)(ValuesSetpointsStates.average_temperature_setpoint * 100));
  zero_Placment(20, (long unsigned int)(ValuesSetpointsStates.blue_luminosity_setpoint * 100));
  zero_Placment(21, (long unsigned int)(ValuesSetpointsStates.red_luminosity_setpoint * 100));
  zero_Placment(30, (long unsigned int)(ValuesSetpointsStates.Kp_blue_led * 100));
  zero_Placment(31, (long unsigned int)(ValuesSetpointsStates.Ki_blue_led * 100));
  zero_Placment(32, (long unsigned int)(ValuesSetpointsStates.Kd_blue_led * 100));
  zero_Placment(33, (long unsigned int)(ValuesSetpointsStates.Kp_red_led * 100));
  zero_Placment(34, (long unsigned int)(ValuesSetpointsStates.Ki_red_led * 100));
  zero_Placment(35, (long unsigned int)(ValuesSetpointsStates.Kd_red_led * 100));
  zero_Placment(36, (long unsigned int)(ValuesSetpointsStates.Kp_pelter_one * 100));
  zero_Placment(37, (long unsigned int)(ValuesSetpointsStates.Ki_pelter_one * 100));
  zero_Placment(38, (long unsigned int)(ValuesSetpointsStates.Kd_pelter_one * 100));
}

void UART::send_Measurments(void)
{
  for (int i = 1; i <= 6; i++) {
    zero_Placment(i, (unsigned int)(ValuesSetpointsStates.temperature_values[i] * 100));
  }
  zero_Placment(7, (unsigned int)(ValuesSetpointsStates.average_temperature * 100));
  zero_Placment(22, (unsigned int)(ValuesSetpointsStates.blue_luminosity_value * 100));
  zero_Placment(23, (unsigned int)(ValuesSetpointsStates.red_luminosity_value * 100));
}


void UART::send_System_State(void)
{
  // send al of the device ID and there current state (1 is on, 0 is off) , will have more states eventually

  for (int g = 0; g < 9; g++) {
    zero_Placment(ValuesSetpointsStates.Systemdevice_ID[g], (unsigned int)(ValuesSetpointsStates.state[g] * 100));
  }


}




void UART::variable_Update(void)
{
  // this updates the variables that has been called in the string
  switch (variable_ID) {
    case 15:
      if ((value > 5) && (value < 35))
      {
        ValuesSetpointsStates.average_temperature_setpoint = (double)value; // note all temperature values are multiples by 100 for convinience in UART so must be divided by 100 before applied
      }
      break;
    case 20:
      if ((value > 500) && (value < 65000))
      {
        ValuesSetpointsStates.blue_luminosity_setpoint = (double)(int)value;
      }
      break;
    case 21:
      if ((value > 500) && (value < 65000))
      {
        ValuesSetpointsStates.red_luminosity_setpoint = (double)(int)value;
      }
      break;
    case 30:

      ValuesSetpointsStates.Kp_blue_led = (double)(value);

      break;
    case 31:

      ValuesSetpointsStates.Ki_blue_led = (double)(value);

      break;
    case 32:

      ValuesSetpointsStates.Kd_blue_led = (double)(value);

      break;
    case 33:

      ValuesSetpointsStates.Kp_red_led = (double)(value);

      break;
    case 34:

      ValuesSetpointsStates.Ki_red_led = (double)(value);

      break;
    case 35:

      ValuesSetpointsStates.Kd_red_led = (double)(value);

      break;

    case 36:

      ValuesSetpointsStates.Kp_pelter_one = (double)(value);

      break;
    case 37:

      ValuesSetpointsStates.Ki_pelter_one = (double)(value);

      break;
    case 38:

      ValuesSetpointsStates.Kd_pelter_one = (double)(value);

      break;

    default:

      break;
  }


}




void UART::zero_Placment(unsigned long int value, unsigned long int value_2) { // lenght is correct length of string after _
  // this function ensures the correct number of placeholding zeros are added to serial communcaiton value , then the value is printed
  // first must find the length(number of digits of the variable for the given type
  _type = 1;

  for (byte i = 0; i <= 1; i++)
  {
    _type = !_type; // switch the type so one is run and then the other
    switch (_type) {
      case 0:
        //do something when var equals 1

        if (value < 10)
        {
          _digits = 2;
        }
        else if (value < 100)
        {
          _digits = 1;
        }
        else
        {
          _digits = 0;
        }

        break;
      case 1:
        if (value_2 < 1)
        {
          _digits = 6;
        }
        else if (value_2 < 10)
        {
          _digits = 6;
        }
        else if (value_2 < 100)
        {
          _digits = 5;
        }
        else if (value_2 < 1000)
        {
          _digits = 4;
        }
        else if (value_2 < 10000)
        {
          _digits = 3;
        }
        else if (value_2 < 100000)
        {
          _digits = 2;
        }
        else if (value_2 < 1000000)
        {
          _digits = 1;
        }
        else
        {
          _digits = 0;
        }

        break;
      default:
        // if nothing else matches, do the default
        // default is optional
        _digits = 0;
        break;
    }
    // next print the correct number of zeros

    while (_digits != 0)
    {
      _digits = _digits - 1;
      Serial.print("0");

    }

    if (_type == 1)
    {
      Serial.print(value_2);
      Serial.print("\r\n");
    }
    else if (_type == 0)
    {
      Serial.print(value);
      Serial.print("_");
    }

  }
}


void UART::device_set(byte ID,byte states)
{
  // have got good data, must set a hardware check to returen a message when it has been verified that it has been completed.
//  Serial.println("HWS");
  _valid=1; //debug code
  for (int f = 0; f <9; f++) // check to see if the given device ID is appropiate to this arduino
    {
    if (ValuesSetpointsStates.Systemdevice_ID[f] == device_ID)
    {
      _valid=1;
      break;
    }

  }

 if (_valid ==1) // if it is do work on it.
 {
  PID_main_instance->set_Event(ID, (byte)states, dummy_value);
PID_main_instance->set_Hardware(ID, (byte)states, dummy_value);
 }

}



void UART::bounce_back(String string_in, bool valid)
{
  // this method returns the sent string with an error message depending on wheater the arduino has implemented the action, or whaeter message was invalid or hardware constrained.

  Serial.print(string_in);
  // check whater the given device, vairable ro variable ID is valud and update valid accordingly.
  //

  // else
   Serial.print("_");
  Serial.print(valid);
  Serial.print("\r\n");
  _inputstring=="";

}

