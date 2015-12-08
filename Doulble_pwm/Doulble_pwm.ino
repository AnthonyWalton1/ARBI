//This code implments an improtant function. it switches the pwm off the output pin on and off at a frequency currently set at 500hz.

volatile int state=0; // this variable is gloabl, must be placed before any functions. state is used to determine if pwm is on (1) or off (0).

void setup() {
  // setup the timer registers in the mircoprocessor.
TCCR1B = TCCR1B & 0b11111000 | 0x02;
TCCR2B = TCCR2B & 0b11111000 | 0x01;
TCCR3B = TCCR3B & 0b11111000 | 0x01;
TCCR4B = TCCR4B & 0b11111000 | 0x01;
TCCR5B = TCCR5B & 0b11111000 | 0x01;
// this code here controls the frequency for the particular pins on the timer unit. i.e TCCR2B is for timer unit 2
// 0x01 is 31khz/1
// 0x02 is 31khz/8
// 0x03 is 31khz/64
// 0x04 is 31khz/256
// 0x05 is 31khz/1024

//timer 1 (controls pin 13, 4)
//timer 2 (controls pin 12, 11)
//timer 3 (controls pin 10, 9)
//timer 4 (controls pin 5, 3, 2)
//timer 5 (controls pin 8, 7, 6)

// the timer 1 does generates waveforms of different freqeucnies, as such this timer will be used as the counter for the timer interrupts (this prevents it from being used...
// ... as a pwm source for the leds)

    // set compare match register to desired timer count:
     TIMSK0 = (0<<OCIE0A) | (1<<TOIE0); // enable the timer interrupt for timer unit 1.
     TIMSK1 = _BV(TOIE1); // enable overflow as the type of interrupt used.
 

analogWrite(2,150); // led 1
analogWrite(3,150); // led 2
analogWrite(5,150); // led 3
analogWrite(6,150); // led 4
analogWrite(7,150); // led 5
analogWrite(8,150); // led 6
}


void loop(){
 
}


ISR(TIMER1_OVF_vect){
// this is the interrupt service routine function (note as an interrupt function it can only see global varables)
Serial.print("h");
if (state ==0){ // the pwm is off, turn it on.

  
analogWrite(8,150); // turn it back on



state =1;
}
else { // the pwm is on, turn it off.

  
  digitalWrite(8,LOW);


  
  state = 0;
} 
}



