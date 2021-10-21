/* Some pseudo-code to base the current-sensing system off of (untested)
 *  Assumes an ACS723 is used (Sparkfun current-sensing breakout board)
 *  Author: Gordon Lay, October 2021
 */

// NOTE: THESE VALUES HAVE NOT BEEN TESTED
// These values are based on the 0.1V zero-current output voltage
// and assume 400mV/A sensitivity (see datasheet).
#define LOWER_THRESHOLD 0.5 // 1A current draw
#define UPPER_THRESHOLD 0.7 // 1.5A current draw

const int SENSE_PIN = A4 // analogue pin to measure output from ACS723
float reading;

void setup() {
  Serial.begin(9600);
}

void loop() {
  reading = analogRead(SENSE_PIN);
  if (reading > UPPER_THRESHOLD) {
    // Decrease speed of reel motor via governor
  } else if (reading < LOWER_THRESHOLD) {
    // Increase speed of reel motor via governor
  } 
}
