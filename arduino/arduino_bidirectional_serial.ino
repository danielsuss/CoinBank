#include <Servo.h>

#define LASER_SENSOR_L 0
#define LASER_SENSOR_R 1

#define SERVO_L 2
#define SERVO_R 3

Servo servo_l;
Servo servo_r; 

int l_pos = 180;
int r_pos = 180;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LASER_SENSOR_L, INPUT);
  pinMode(LASER_SENSOR_R, INPUT);
  servo_l.attach(SERVO_L);
  servo_r.attach(SERVO_R);
  servo_l.write(l_pos);
  servo_r.write(r_pos);
}

void loop() {

  byte left_sensor_state = digitalRead(LASER_SENSOR_L);
  byte right_sensor_state = digitalRead(LASER_SENSOR_R);
  
  /// Write out serial output when laser is triggered
  if (left_sensor_state == HIGH) {
    Serial.write(60);
  }
  if (right_sensor_state == HIGH) {
    Serial.write(61);
  }

  /// Read serial input
  if (Serial.available() > 0) {
    int servo_number = Serial.read() - '0';

    switch (servo_number) {
      case 0:
        servo_l.write(15);
        delay(15);
        servo_l.write(0);
        break;
      case 1:
        servo_r.write(-15);
        delay(15);
        servo_r.write(15);
        break;
    } 
  }
}