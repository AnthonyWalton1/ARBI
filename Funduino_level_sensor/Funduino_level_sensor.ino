  // Declare analog pin
  int analogPin = 0;

  int val;

void setup() {
  // put your setup code here, to run once:

  // Start serial com
  Serial.begin(9600);

  // Set analog pin mode (input)
  pinMode(analogPin, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

  // Read analog pin
  val = analogRead(analogPin); // default analoge read setting is 10bit resolution of voltage (0 to 1023) from 0v to 5 v respectivly

  // Print analog reading
  Serial.println(val);

  // Pause for 1 second before repeating
}

// ******************************** Data ********************************* //

// S is data
// + is power supply (5V)
// - is GND

// Default settings for analog reading returns a 10 bit values (0 to 1023) based upon voltage readings between 0 to 5 V (0 corresponds to 0 V and 1023 corresponds to 5 V)

// ********************************************************************** //
