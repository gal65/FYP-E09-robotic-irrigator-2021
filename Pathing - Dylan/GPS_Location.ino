#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>

/*
   This sample sketch demonstrates the normal use of a TinyGPS++ (TinyGPSPlus) object.
   It requires the use of SoftwareSerial, and assumes that you have a
   9600-baud serial GPS device hooked up on pins 8(rx) and 9(tx) and a HMC5883 Magnetic Compass
   connected to the SCL/SDA pins.
*/

static const int RXPin = 16, TXPin = 17;
static const uint32_t GPSBaud = 9600;
static const int GPSPoints = 10;

// Assign a Uniquej ID to the HMC5883 Compass Sensor
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

// The TinyGPS++ object
TinyGPSPlus gps;

// The serial connection to the NEO-6m GPS module
SoftwareSerial ss(RXPin, TXPin);
float location_array[2][GPSPoints] = { {43.52052368448694, -43.52052368448694, -43.52052368448694, 4, 5, 6, 7, 8, 9, 10 },
                       { 172.58391852158596, 172.58394074378594, 172.58396296598596, 14, 15, 16, 17, 18, 19, 20 }};
int irrigating_array[GPSPoints] = {1, 1, 1, 0, 0, 0, 0, 0, 1, 1}; //1 if irrigating, 0 if not irrigating
int direction_array[GPSPoints] = {1, 1, 1, 0, 0, 0, 0, 0, 1, 1};

         
float current_lat = 0;
float current_long = 0;
int next_index = 0;
int max_index = 10;
float NeededBearing = 0;

void displaySensorDetails(void)
{
  sensor_t sensor;
  mag.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" uT");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" uT");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" uT");  
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}

void setup()
{
  Serial.begin(115200);
  Serial.println("Initilising");
  ss.begin(GPSBaud);

  Serial.println(F("Simple Test with TinyGPS++ and attached NEO-6M GPS module"));
  Serial.print(F("Testing TinyGPS++ library v. ")); Serial.println(TinyGPSPlus::libraryVersion());
  Serial.println();
  displaySensorDetails();
}


//Need to get an array of points
//On startup determine what is the closest point
//Follow array until completed
//For each point determine the distance away from the next point and the bearing needed to get there
//loop

void loop()
{
  int gps_checked = check_gps(); //gets information from gps
  if (gps_checked) {
    check_point();
  }
}

void check_point()
{
  float next_lat = location_array[0][next_index];
  float next_long = location_array[1][next_index];
  
  float relative_lat = abs(current_lat - next_lat);
  float relative_long = abs(current_long - next_long);
  
  float relative_lat_meters = relative_lat/0.0000111111;
  float relative_long_meters = relative_long/0.000011111;

  float current_radian = pow((pow(relative_lat_meters, 2)+pow(relative_long_meters, 2)), 0.5);
  NeededBearing = atan2(relative_lat_meters, relative_long_meters)* 57296 / 1000;

  if (current_radian > 100000) {
    Serial.println("No Location Known");
  }

  else {
    Serial.print("lat meters: "); Serial.println(relative_lat_meters);
    Serial.print("long meters: "); Serial.println(relative_long_meters);
    Serial.print("Distance to Next Points: "); Serial.println(current_radian);
    Serial.print("Needed Bearing: "); Serial.println(NeededBearing);
    Serial.print("Current index: "); Serial.println(next_index);
  }
  
  if ((relative_lat_meters < 5) and (relative_long_meters < 5)) {
    next_index++;
    if (next_index >= max_index)
      next_index = 0;

    //Need to recalculate if we are considered at the point
    next_lat = location_array[0][next_index];
    next_long = location_array[1][next_index];
  }

  print_direction();
  print_irrigating();
}

void print_direction() {
  if (direction_array[next_index]) {
    Serial.println("Going Fowards");
  }

  else {
    Serial.println("Going Backwards");
  }
}

void print_irrigating() {
  if (irrigating_array[next_index]) {
    Serial.println("Irrigating on");
  }

  else {
    Serial.println("Irrigating off");
  }
}

int check_gps()
{
  int return_val = 0;
  while (ss.available() > 0)
    if (gps.encode(ss.read())) {
      displayGpsInfo();
      return_val = 1;
    }
    return(return_val);
}

void displayGpsInfo()
{
  // Prints the location if lat-lng information was recieved
  Serial.print(F("Location: ")); 
  if (gps.location.isValid())
  {
    Serial.print(gps.location.lat(), 6);
    current_lat = gps.location.lat();
    Serial.print(F(","));
    Serial.print(gps.location.lng(), 6);
    current_long = gps.location.lng();
  }
  // prints invalid if no information was recieved in regards to location.
  else
  {
    Serial.print(F("INVALID"));
  }

  Serial.print(F("  Date/Time: "));
  // prints the recieved GPS module date if it was decoded in a valid response.
  if (gps.date.isValid())
  {
    Serial.print(gps.date.month());
    Serial.print(F("/"));
    Serial.print(gps.date.day());
    Serial.print(F("/"));
    Serial.print(gps.date.year());
  }
  else
  {
    // prints invalid otherwise.
    Serial.print(F("INVALID"));
  }

  Serial.print(F(" "));
  // prints the recieved GPS module time if it was decoded in a valid response.
  if (gps.time.isValid())
  {
    if (gps.time.hour() < 10) Serial.print(F("0"));
    Serial.print(gps.time.hour());
    Serial.print(F(":"));
    if (gps.time.minute() < 10) Serial.print(F("0"));
    Serial.print(gps.time.minute());
    Serial.print(F(":"));
    if (gps.time.second() < 10) Serial.print(F("0"));
    Serial.print(gps.time.second());
    Serial.print(F("."));
    if (gps.time.centisecond() < 10) Serial.print(F("0"));
    Serial.print(gps.time.centisecond());
  }
  else
  {
    // Print invalid otherwise.
    Serial.print(F("INVALID"));
  }
  Serial.println();
  if(mag.begin())
  {
    displayCompassInfo();
  }
}

void displayCompassInfo()
{
  /* Get a new sensor event */ 
  sensors_event_t event; 
  mag.getEvent(&event);
 
  /* Display the results (magnetic vector values are in micro-Tesla (uT)) */
  Serial.print("X: "); Serial.print(event.magnetic.x); Serial.print("  ");
  Serial.print("Y: "); Serial.print(event.magnetic.y); Serial.print("  ");
  Serial.print("Z: "); Serial.print(event.magnetic.z); Serial.print("  ");

  // Correcting for the magentic field in christchurch in rad
  float heading = atan2(event.magnetic.y, event.magnetic.x);
  float declinationAngle = 0.42;
  heading += declinationAngle;
  
  // Correct for when signs are reversed.
  if(heading < 0)
    heading += 2*PI;
    
  // Check for wrap due to addition of declination.
  if(heading > 2*PI)
    heading -= 2*PI;
   
  // Convert radians to degrees for readability.
  float headingDegrees = heading * 180/M_PI; 
  
  Serial.print("Magnetic heading (degrees): "); Serial.println(headingDegrees);
  Serial.print("Change Headings (degrees): "); Serial.println(headingDegrees-NeededBearing);
  
  delay(500);
}

//Need to implimenat using heading and fixing magnetometer crash
//Work on generating a path
//Need to write comments
//Need to handle multiple arrays
