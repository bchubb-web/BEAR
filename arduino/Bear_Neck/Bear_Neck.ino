#include <Servo.h>

Servo neck;
//define a servo object as neck

int pos = 90;
//start with the head facing forwards

void setup() {
  neck.attach(9);
  //define pin 9 for the servo control
  Serial.begin(9600);
  //start serial 
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()> 0){
    char data = Serial.read();
    Serial.println(data);
    //get serial data
    if (data == '9' && pos > 0){
      //decrease position
      Serial.println("right");
      pos-=2;
    }
    else if(data == '6' && pos < 180){
      Serial.println("left");
      //increase posotion
      pos+=2;
    }
    neck.write(pos);
   } 
}
