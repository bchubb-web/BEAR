#include <Servo.h>

Servo mouthServo

int position = 0

void setup(){
    Serial.begin(9600);
    mouthServo.attach(9);
}

void open(){
    for (position = 0; position <= 90; position+=1){
    mouthServo.write(position);
    delay(15)
    }
}


void close(){
    for(position = 90; position >= 0; position+=1){
        mouthServo.write(position);
        delay(15);
    }
}

void loop(){
    if (Serial.available()>0){
        char data = Serial.read();
        if(data=='1'){open()}
        if(data=="2"){close()}
    }

}