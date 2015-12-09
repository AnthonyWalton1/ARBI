// we could make it so that we have a list of possbile data to be given at simply check the list.
//e.g list
//list 1 = setpint 1 set
//list 2 = setpoint 2 set
// lst 3 = luminosity 1 set

String inputString = "";         // a string to hold incoming data
boolean stringComplete = 0;  // whether the string is complete

void setup() {
  // initialize serial:
  Serial.begin(9600);
  inputString.reserve(400);
}

void loop() {
  serialEvent(); //call the function
  // print the string when a newline arrives:






  
  if (stringComplete) {
// have succesfullt recieved a string, now must get out the important data.



    
    Serial.println(inputString);
    // clear the string:
    Serial.println(inputString[0]);

    inputString = "";
    stringComplete = false;
  }




  
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == 91) {
      stringComplete = true;
    }
  }
}
