const int ledPin = 13;

void setup() {
  
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  
}

void loop() {
  
  if (Serial.available() == 1) {
    light(Serial.read() - '0');
  }
  
  delay(500);

}

void light(int PiNum) {
  for (int i = 0; i < PiNum; i++) {
    digitalWrite(ledPin, HIGH);
    delay(100);
    digitalWrite(ledPin, LOW);
    delay(100);
  }
}
