#include <SoftwareSerial.h> 
#include "Wire.h"  //가속도
#include <MPU6050_light.h> 
MPU6050 mpu(Wire); 
SoftwareSerial HC06(2, 3); 

String data;
int state = 0;
int state2 = 0;
int m = 4;
int green = 6;
int red = 7;
int trig = 8;
int echo = 9;
int piezo = 11;
int ir2 = 12;
int ir = 13;

void setup() {
  pinMode(ir, INPUT);
  pinMode(ir2, INPUT);
  pinMode(m, OUTPUT);
  pinMode(green,OUTPUT);
  pinMode(red,OUTPUT);
  pinMode(trig,OUTPUT);
  pinMode(echo,INPUT);
  pinMode(piezo, OUTPUT);
  Serial.begin(9600);
  HC06.begin(9600);
  Wire.begin();

  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while(status!=0){ } 
  
  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  mpu.calcOffsets(true,true); 
  Serial.println("Done!\n");
}

void loop() {
  if(HC06.available()){
    data = HC06.readStringUntil(0x0A);
  }
  if(data == "connected"){
    mpu.update();
    if(mpu.getGyroZ()<-5){
      float Length, distance;
      digitalWrite(trig, LOW);
      delay(2);
      digitalWrite(trig, HIGH);
      delay(10);
      digitalWrite(trig, LOW);
      Length = pulseIn(echo, HIGH);
      distance = ((float)(340 * Length) / 10000) / 2;
      if(distance <= 24 and distance >= 5){
        digitalWrite(red, HIGH);
        digitalWrite(green, LOW);
        state = digitalRead(ir);
        state2 = digitalRead(ir2);
        
        if(state == 0 or state2 == 0 ){
          digitalWrite(m, HIGH);
          tone(piezo, 523, 500);
          HC06.println("위험상황 발생");
          digitalWrite(red, HIGH);
          digitalWrite(green, LOW);
          delay(3000);
          digitalWrite(m, LOW);
          HC06.println("");
          digitalWrite(red, LOW);
          digitalWrite(green, HIGH);
          }
        }
    }
    }else{
      digitalWrite(green, LOW);
      digitalWrite(red, LOW);
      digitalWrite(trig, LOW);
      digitalWrite(m, LOW);
      }
 

}
