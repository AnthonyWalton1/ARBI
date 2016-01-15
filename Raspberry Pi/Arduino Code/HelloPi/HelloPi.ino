// Port for Arduino on Pi is ACM0


void setup() {
  
Serial.begin(9600);

}

void loop() {
  
  Serial.println("Hello Pi\r\n");
  
 delay(2000);
 
}
