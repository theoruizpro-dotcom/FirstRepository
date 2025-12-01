bool startLoop = false;


void setup() {
 // put your setup code here, t
 pinMode (LED_BUILTIN, OUTPUT);
 digitalWrite(LED_BUILTIN, LOW);
 Serial.begin(1000000, SERIAL_8N1);
 while(!startLoop) {
   if(Serial.available()) {
    startLoop = ((char) (Serial.read()) == 'r');
   }
 }
}


void loop() {
 // put your main code here, to run repeatedly:
 digitalWrite(LED_BUILTIN, HIGH);
 }
