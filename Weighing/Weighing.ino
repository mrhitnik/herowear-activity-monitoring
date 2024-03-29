#include <Arduino.h>
#include "HX711.h"

const int LOADCELL_DOUT_PIN = 5;
const int LOADCELL_SCK_PIN = 6;

HX711 scale;

void setup()
{

  // Initializing arduino and pins  
  
  Serial.begin(9600);

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);

  scale.tare(); // reset the scale to 0
}

void loop()
{
  scale.set_scale(10481.51);  // Change this value to calibrate the load cell if needed

  double reading = scale.get_units();

  if (reading < 0) { reading *= -1; }   // To only print the positive values and ignore values such as -0

  Serial.println(reading);

  delay(1);
}
