int in1 = 25;
int in2 = 24;
int in3 = 23;
int in4 = 18;

int en1 = 12;
int en2 = 16;

String command;
String speed;
String turnAngle;

void setup() {
  pinMode(in1, OUTPUT); // Set pins as outputs
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(en1, OUTPUT);
  pinMode(en2, OUTPUT);

  analogWrite(en1, 0); // Initially set motor speeds to 0
  analogWrite(en2, 0);

  Serial.begin(9600); // Initialize serial communication
}

void drive(int speed, int turnAngle) {
  int speedL = (speed + turnAngle) / 2;
  int speedR = (speed - turnAngle) / 2;

  // Ensure speedL and speedR are within the valid range
  if (speedL > 100) {
    speedL = 100;
  }
  else if (speedL < -100) {
    speedL = -100;
  }

  if (speedR > 100) {
    speedR = 100;
  }
  else if (speedR < -100) {
    speedR = -100;
  }

  analogWrite(en1, abs(speedL)); // Set motor speeds
  analogWrite(en2, abs(speedR));

  // Set motor directions
  if (speedL > 0) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  }
  else if (speedL < 0) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  }

  if (speedR > 0) {
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
  }
  else if (speedR < 0) {
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
  }
  else {
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
  }
}

void stop() {
  analogWrite(en1, 0); // Stop the motors
  analogWrite(en2, 0);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void loop() {
  if (Serial.available()) {
    command = Serial.readStringUntil('\n'); // Read a line from serial
    if (command.indexOf("pls stop") != -1) {
      stop();
    }
    else if (command.indexOf("pls drive") != -1) {
      Serial.println("ok speed?"); // Send a response to Raspberry Pi
      while (!Serial.available()) {} // Wait for input from Raspberry Pi
      speed = Serial.readStringUntil('\n'); // Read speed value
      Serial.println("ok, turnAngle?"); // Send another response
      while (!Serial.available()) {} // Wait for input from Raspberry Pi
      turnAngle = Serial.readStringUntil('\n'); // Read turnAngle value
      
      drive(speed.toInt(), turnAngle.toInt()); // Convert strings to integers and call the drive function
    }
    else {
      Serial.println("huh");
    }
  }
}