const int voltageControllerPin = 9;
const int currentControllerPin = 10;
const int currentIndicatorPin = A0;
const int pressureIndicatorPin = A1;


double targetVoltage;
double targetCurrent;


void setup() {
  Serial.begin(9600);
  pinMode(voltageControllerPin, OUTPUT);
  pinMode(currentControllerPin, OUTPUT);
}


void loop() {
  String cmd = Serial.readString();
  if (cmd.length() != 0) {
    if (cmd.startsWith("SET_SOLENOID_VOLTAGE")) {
      // SET VOLTAGE
      double value = cmd.substring(20).toFloat();
      //if (value < 0 || value > 100) {
      //  Serial.println("ERROR: target voltage out of range (expected a value between 0 and 100 volts)");
      //  return;
      //}
      targetVoltage = value;
      int analogValue = round((targetVoltage / 100) * 255);
      if (analogValue < 0)
        analogValue = 0;
      else if (analogValue > 255)
        analogValue = 255;
      analogWrite(voltageControllerPin, analogValue);
      Serial.println("Done");
    }
    else if (cmd.startsWith("GET_SOLENOID_VOLTAGE")) {
      // GET VOLTAGE
      Serial.println(targetVoltage);
    }
    else if (cmd.startsWith("SET_SOLENOID_CURRENT")) {
      // SET CURRENT
      double value = cmd.substring(20).toFloat();
      //if (value < 0 || value > 100) {
      //  Serial.println("ERROR: target current out of range (expected a value between 0 and 100 amps)");
      //  return;
      //}
      targetCurrent = value;
      int analogValue = round((targetCurrent / 100) * 255);
      if (analogValue < 0)
        analogValue = 0;
      else if (analogValue > 255)
        analogValue = 255;
      analogWrite(currentControllerPin, analogValue);
      Serial.println("Done");
    }
    else if (cmd.startsWith("GET_TARGET_SOLENOID_CURRENT")) {
      // GET CURRENT
      Serial.println(targetCurrent);
    }
    else if (cmd.startsWith("GET_SOLENOID_CURRENT")) {
      // READ CURRENT
      Serial.println(0.1105 * analogRead(currentIndicatorPin) + 0.4321);
    }
    else if (cmd.startsWith("PING")) {
      // PING
      Serial.println("ok");
    }
    else if (cmd.startsWith("GET_PRESSURE")) {
      Serial.println(getPressure());
    }
    else
      Serial.println("ERROR: unknown command");
  }
}


float getPressure(){
  int i = 0;
  float voltagesum = 0;
  while (i < 25 ){
    float volt = analogRead(pressureIndicatorPin);
    volt = volt * (5.0/1024.0);
    voltagesum += volt;
    i += 1;
  }
  float voltavg = voltagesum / 25.0;
  float pressure = (voltavg - 1.06)/0.496; //r=1, ignored smallest pressure values
  return(pressure);
}
