#include <Servo.h>

Servo servoX;  // Left-Right movement
Servo servoY;  // Up-Down movement
int posX = 90;  // Initial position at 90 degrees
int posY = 90;

void setup() {
  Serial.begin(9600);
  servoX.attach(9);  // X-axis servo motor pin
  servoY.attach(10); // Y-axis servo motor pin
  servoX.write(posX);
  servoY.write(posY);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int commaIndex = data.indexOf(',');
    int angleX = data.substring(0, commaIndex).toInt();
    int angleY = data.substring(commaIndex + 1).toInt();

    if (angleX >= 0 && angleX <= 180) {
      servoX.write(angleX);
      posX = angleX;
    }
    if (angleY >= 0 && angleY <= 180) {
      servoY.write(angleY);
      posY = angleY;
    }
  }
}
