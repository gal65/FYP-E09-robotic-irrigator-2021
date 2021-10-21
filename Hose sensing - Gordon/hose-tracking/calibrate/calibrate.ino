#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = A0;
const int LOADCELL_SCK_PIN = A1;
int mass;
float reading;

HX711 load_cell;

void setup() {
  Serial.begin(9600);
  Serial.println("Start");
  // Initialize library with data output pin, clock input pin and gain factor.
  // Channel selection is made by passing the appropriate gain:
  // - With a gain factor of 64 or 128, channel A is selected
  // - With a gain factor of 32, channel B is selected
  // By omitting the gain factor parameter, the library
  // default "128" (Channel A) is used here.
  load_cell.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  load_cell.set_gain(128); // use channel A
  Serial.println("-----------------------------------------");
  load_cell.set_scale();
  load_cell.tare();
  Serial.println("What is the known mass? (type into serial monitor and press Enter)");
  while (Serial.available() == 0) {
    // Wait for user to input data
  }
  mass = Serial.parseInt();
  Serial.println("Place known mass now");
  delay(5000);
  reading = load_cell.get_units(10);
  Serial.print("Raw reading:\t");
  Serial.println(reading);
  Serial.print("Calculated scale factor:\t");
  Serial.println(reading/mass);
  Serial.print("Done. (hard reset board to run again until output is 1)");
}

void loop() {
}
