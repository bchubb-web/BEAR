#define A 2
#define B 3
#define C 4
#define D 5

#define NUMBER_OF_STEPS_PER_REV 16
//rotations the internal motor is making, as 512 makes the external head go 360^0
//1/32 of a full rotation
void setup() {
  Serial.begin(9600);
  //start serial reading
  pinMode(A,OUTPUT);
  pinMode(B,OUTPUT);
  pinMode(C,OUTPUT);
  pinMode(D,OUTPUT);
  //set the pins for the stepper motor
}

void write(int a,int b,int c,int d){
  //send the data for each electromagnet to be on or off
digitalWrite(A,a);
digitalWrite(B,b);
digitalWrite(C,c);
digitalWrite(D,d);
}

void leftStep(){
  //magnet orangement for clockwise turning
  int i = 0;
  while(i<NUMBER_OF_STEPS_PER_REV){
  write(0,0,0,1);
  delay(2);
  write(0,0,1,1);
  delay(2);
  write(0,0,1,0);
  delay(2);
  write(0,1,1,0);
  delay(2);
  write(0,1,0,0);
  delay(2);
  write(1,1,0,0);
  delay(2);
  write(1,0,0,0);
  delay(2);
  write(1,0,0,1);
  delay(2);
  i++;
}}

void rightStep(){
int i = 0;
while(i<NUMBER_OF_STEPS_PER_REV){
   //magnet orangement for anti-clockwise turning
write(1,0,0,0);
delay(2);
write(1,1,0,0);
delay(2);
write(0,1,0,0);
delay(2);
write(0,1,1,0);
delay(2);
write(0,0,1,0);
delay(2);
write(0,0,1,1);
delay(2);
write(0,0,0,1);
delay(2);
write(1,0,0,1);
delay(2);
i++;
}
}


void loop() {

  if (Serial.available() > 0) {
    //if there is data send over serial
    char data = Serial.read();
    //get sent data
    //Serial.println(data);
    //return data

     switch(data){
      case '9':
        rightStep();
        break;
     
     case '6':
        leftStep();
        break;

     default:
        //reset motor magnets
        write(0,0,0,0);
        //delay 1 microsecond
        delay(2);
        break;
     }
    if (data == '6'){
      //if the data is the code for left
      Serial.println("left<<");
      leftStep();
    }
    if (data == '9'){
      //if the data is the code for right
      Serial.println("right>>");
      rightStep();
    }
  }
}
