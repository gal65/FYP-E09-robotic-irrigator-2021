/* A program to read from one load cell and display the output in serial every second.
 *  Author: Gordon Lay, October 2021
 */

#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = A0;
const int LOADCELL_SCK_PIN = A1;

HX711 load_cell;

void setup() {
  Serial.begin(9600);
  Serial.println("Read from load cell");
  Serial.println("Initializing the load cell");

  // Initialize library with data output pin, clock input pin and gain factor.
  // Channel selection is made by passing the appropriate gain:
  // - With a gain factor of 64 or 128, channel A is selected
  // - With a gain factor of 32, channel B is selected
  // By omitting the gain factor parameter, the library
  // default "128" (Channel A) is used here.
  load_cell.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  load_cell.set_gain(128); // use channel A
  Serial.println("-----------------------------------------");
  Serial.println("Before setting up the load cell:");
  Serial.print("read: \t\t");
  Serial.println(load_cell.read());             // print a raw reading from the ADC
 
  Serial.print("read average: \t\t");
  Serial.println(load_cell.read_average(20));   // print the average of 20 readings from the ADC

  Serial.print("get value: \t\t");
  Serial.println(load_cell.get_value(5));       // print the average of 5 readings from the ADC minus the tare weight (not set yet)

  Serial.print("get units: \t\t");
  Serial.println(load_cell.get_units(5), 1);    // print the average of 5 readings from the ADC minus tare weight (not set) divided
                                                // by the SCALE parameter (not set yet)

  load_cell.set_scale(5262.57);                 // this value is obtained by calibrating the scale with known weights; see the README for details
  load_cell.tare();                             // reset the scale to 0

  Serial.println("-----------------------------------------");

  Serial.println("After setting up the left load cell:");

  Serial.print("read: \t\t");
  Serial.println(load_cell.read());                 // print a raw reading from the ADC

  Serial.print("read average: \t\t");
  Serial.println(load_cell.read_average(20));       // print the average of 20 readings from the ADC

  Serial.print("get value: \t\t");
  Serial.println(load_cell.get_value(5));   // print the average of 5 readings from the ADC minus the tare weight, set with tare()

  Serial.print("get units: \t\t");
  Serial.println(load_cell.get_units(5), 1);        // print the average of 5 readings from the ADC minus tare weight, divided
            // by the SCALE parameter set with set_scale
  Serial.println("-----------------------------------------");
  Serial.println("Readings:");
}

void loop() {
  Serial.print("reading:\t");
  Serial.print(-(load_cell.get_units()), 1);
  Serial.println(" N");
  //load_cell.power_down(); // put the ADC in sleep mode       
  delay(1000);
  //load_cell.power_up();
}
