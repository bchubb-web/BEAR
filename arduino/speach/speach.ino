int PowerPin = 12;               

void setup(){
  pinMode(PowerPin, OUTPUT);     
}

void loop(){
  digitalWrite(PowerPin, HIGH);
  delay(1000); 
  digitalWrite(PowerPin, LOW);
  delay(1000); 
}
