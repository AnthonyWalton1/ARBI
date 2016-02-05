#include <stdio.h>
#include <string.h>

// Code sends back a successful (=1) handshake string for the particular pump that was received when string starts with 1
// Code sends back the latest machineState when string starts with 2. The machineState is instantly updated correcty with 
// the value contained in the handshake string, everytime a handshake command is sent


// Define global variables here
String inputString = "";
int machineStates[1];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  machineStates[0] = 0;
}

void loop() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if ((inChar != 10) && (inChar != 13)) {
      inputString += inChar;
    }
    
    if (inChar == 10){     // 64 is ASCII for @, 10 is for \n
      sortInput();
      inputString = "";
    }
  }
}

void sortInput(){
  char charInString;
  String inputType = "";
  String componentID = "";
  String componentValueToSet = "";
  int previousUnderscoreIndex = 0;
  
  for (int i = 0; i < inputString.length(); i++) {
    charInString = inputString[i];
    if (charInString != 95) {
      inputType += charInString;
    } else {
      previousUnderscoreIndex = i;
      break;
    }
  }

  if (inputType == "1") {
    //Serial.println(inputType);

    for (int i = previousUnderscoreIndex+1; i < inputString.length(); i++) {
      charInString = inputString[i];
      if (charInString != 95) {
        componentID += charInString;
      } else {
        previousUnderscoreIndex = i;
        break;
      }
    }

    //Serial.println(componentID);
    
    for (int i = previousUnderscoreIndex+1; i < inputString.length(); i++) {
      charInString = inputString[i];
      if (charInString != 13) {
        componentValueToSet += charInString;
      } else {
        break;
      }
    }

    //Serial.println(componentValueToSet);

    Serial.print("1_" + componentID + "_1\r\n");

    if (componentID == "P103") {
      machineStates[0] = componentValueToSet.toInt();
    }
  }

  if (inputType == "2") {
    Serial.print("2_P103_" + (String)machineStates[0] + "\r\n");
  }
  
}
