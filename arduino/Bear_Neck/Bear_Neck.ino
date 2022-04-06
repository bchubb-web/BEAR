#include <Servo.h>

Servo neck;

int pos = 90;




void setup() {
  // put your setup code here, to run once:
  neck.attach(9);
  Serial.begin(9600);
  /*
  neck.write(0);
  delay(500);
  neck.write(180);
  delay(1000);
  neck.write(90);
  delay(400);*/
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()> 0){
    char data = Serial.read();
    Serial.println(data);
    //Serial.println("pos:"+pos);
    
    if (data == '9' && pos > 0){
      //rightStep();
      Serial.println("right");
      pos-=4;
    }
    else if(data == '6' && pos < 180){
      Serial.println("left");
      //leftStep();
      pos+=4;
    }
    neck.write(pos);
   }  
    /*else{
      if(pos < 90 && pos >= 0){
        pos+=4;
      }
      else if(pos <= 180 && pos > 90){
        pos-=4;
      }
    }
    neck.write(pos);
    
    /*
switch(data){
      case '9':
        rightStep();
        break;
     
     case '6':
        leftStep();
        break;

     default:
     if(pos < 90 && pos >= 0){
      leftStep();
     }
     else if(pos <= 180 && pos > 90){
      rightStep();
     }
        //break;
     }*/
  

}
