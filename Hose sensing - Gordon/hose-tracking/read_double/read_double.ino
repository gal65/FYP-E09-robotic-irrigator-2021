// TODO: Add functionality to send output signals to control MCU (commented out)

#include "HX711.h"

#define THRESHOLD 75      // Force difference threshold, in Newtons
#define TERMS 10          // Number of terms used in taking average measurement
#define SLEEP_TIME 1000   // Time to power down ADC (in milliseconds)

class load_cell {  
  public:
  int DOUT_PIN;
  int SCK_PIN;
  int GAIN;
  float SCALE_FACTOR;
  // int OUTPUT_PIN;
};

load_cell L, R;
HX711 load_cell_L, load_cell_R;
float force_L, force_R;

void load_cell_init() {
  L.DOUT_PIN = A0;
  L.SCK_PIN = A1;
  L.GAIN = 128;
  L.SCALE_FACTOR = 5262.57;
  R.DOUT_PIN = A2;
  R.SCK_PIN = A3;
  R.GAIN = 128;
  R.SCALE_FACTOR = 5262.57;
  
  // L.OUTPUT_PIN = 11;
  // R.OUTPUT_PIN = 13;
  // pinMode(L.OUTPUT_PIN, OUTPUT);
  // pinMode(R.OUTPUT_PIN, OUTPUT);
  // digitalWrite(L.OUTPUT_PIN, LOW);
  // digitalWrite(R.OUTPUT_PIN, LOW);
}

void amp_init() {
  load_cell_L.begin(L.DOUT_PIN, L.SCK_PIN);
  load_cell_L.set_gain(L.GAIN);             
  load_cell_L.set_scale(L.SCALE_FACTOR);   
  load_cell_L.tare();
  load_cell_R.begin(R.DOUT_PIN, R.SCK_PIN);
  load_cell_R.set_gain(R.GAIN);             
  load_cell_R.set_scale(R.SCALE_FACTOR);   
  load_cell_R.tare();
}

void check_forces(float L, float R) {
  // Compare force readings
  if (abs(force_L - force_R) > THRESHOLD) {
    if (force_L < force_R) {
      // Output to control
      // digitalWrite(tracking_output_L, LOW);
      // digitalWrite(tracking_output_R, HIGH);
      Serial.println("Hose tending RIGHT");
    } else if (force_L > force_R) {
      // Output to control
      // digitalWrite(tracking_output_L, HIGH);
      // digitalWrite(tracking_output_R, LOW);
      Serial.println("Hose tending LEFT");
    }
  } else {
    // Output to control
    // digitalWrite(tracking_output_L, LOW);
    // digitalWrite(tracking_output_R, LOW);
    Serial.println("Correct course"); 
  }
}

void toggle_power(int period) {
  load_cell_L.power_down(); 
  load_cell_R.power_down();  
  delay(period);
  load_cell_L.power_up();
  load_cell_R.power_up();
}

void setup() {
  Serial.begin(9600);
  Serial.println("-----------------------------------------");
  Serial.println("Starting up...");
  load_cell_init();
  amp_init();
  Serial.println("Ready.");
  Serial.println("-----------------------------------------");
  Serial.println("Start:");
}

void loop() {
  force_L = -load_cell_L.get_units();
  force_R = -load_cell_R.get_units();
  //  Uncomment to view readings (in case threshold needs adjusting)
  Serial.print(force_L);
  Serial.print("\t");
  Serial.println(force_R);
  check_forces(force_L, force_R);
  toggle_power(SLEEP_TIME);
}
