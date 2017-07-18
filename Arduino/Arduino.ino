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
    if (cmd.startsWith("SET_VOLT")) {
      // SET VOLTAGE
      double value = cmd.substring(9).toFloat();
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
    }
    else if (cmd.startsWith("GET_VOLT")) {
      // GET VOLTAGE
      Serial.println(targetVoltage);
    }
    else if (cmd.startsWith("SET_CURR")) {
      // SET CURRENT
      double value = cmd.substring(9).toFloat();
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
    }
    else if (cmd.startsWith("GET_CURR")) {
      // GET CURRENT
      Serial.println(targetCurrent);
    }
    else if (cmd.startsWith("READ_CURR")) {
      // READ CURRENT
      Serial.println(0.1105 * analogRead(currentIndicatorPin) + 0.4321);
    }
    else if (cmd.startsWith("PING")) {
      // PING
      Serial.println("ok");
    }
    else if (cmd.startsWith("GET_PRESSURE")) {
      Serial.println(analogRead(pressureIndicatorPin));
    }
    else
      Serial.println("ERROR: unknown command");
  }
}
