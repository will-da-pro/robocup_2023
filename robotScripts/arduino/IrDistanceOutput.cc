#include <SharpIR.h>

#define IR A0
#define model 1080 

SharpIR SharpIR(IR, model);
void setup() {
  Serial.begin(9600);
}

void loop() {
  delay(50);
  int dis=SharpIR.distance();
  Serial.print("Distance: ");
  Serial.println(dis);
  Serial.print("Raw reading: ");
  Serial.println(analogRead(A0));
}