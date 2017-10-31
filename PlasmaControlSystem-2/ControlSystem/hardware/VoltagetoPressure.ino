// read a voltage from arduino board, return pressure measurement 

float getPressure(){
  int i=0;
  float voltagesum=0;
  while (i<25){
    float volt=analogRead(A4);
    volt=volt*(5.0/1024.0);
    voltagesum+=volt;
    i+=1;
  }
  float voltavg=voltagesum/25.0; 
  float logpressure=(voltavg - 1.06)/0.496; //r=1, ignored smallest pressure values
  float pressure=pow(10,(logpressure-8)); //converts from log scale 
  return(pressure);  
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()>0){
    char input=Serial.read();
  if (input=='p'){
    float pressure=getPressure();
    Serial.println(pressure,10);
  }}
  delay(10); 

}



