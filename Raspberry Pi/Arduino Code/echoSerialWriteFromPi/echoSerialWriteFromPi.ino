String inputString = "";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;

    if (inputString != "") {
      Serial.print(inputString);
    }

    inputString = "";
  }
}
