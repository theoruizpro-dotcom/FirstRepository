#include "SRF05.h"

const uint8_t TRIGGER_PIN = 7;
const uint8_t ECHO_PIN    = 8;
SRF05 SRF(TRIGGER_PIN, ECHO_PIN);

bool startLoop   = false;
bool restart     = false;
bool firstLoop   = true;

unsigned long initTime, time_us;
float times[100];        // tableau pour stocker les temps en secondes
float distances[100];    // tableau pour stocker les distances en cm
int index = 0;
char serialMessage[64];

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  Serial.begin(1000000, SERIAL_8N1);

  while (!startLoop) {
    if (Serial.available()) {
      startLoop = ((char)(Serial.read()) == 'r');
    }
  }

  SRF.setSpeedOfSound(340);
  SRF.setModeSingle();
}

void loop() {
  if (firstLoop) {
    digitalWrite(LED_BUILTIN, HIGH);
    firstLoop = false;
    initTime  = micros();
    time_us   = 0;
  } else {
    time_us = micros() - initTime;
  }

  if (Serial.available()) {
    restart = ((char)(Serial.read()) == 's');
    if (restart) __NVIC_SystemReset();
  }

  // Lecture du temps (en secondes) et de la distance (en cm)
  times[index] = (float)time_us / 1000000.0;         // conversion microsecondes → secondes
  distances[index] = SRF.getCentimeter();            // lecture distance

  // Envoi des deux valeurs via sprintf et Serial.println
  sprintf(serialMessage, "%.6f,%.2f", times[index], distances[index]);
  Serial.println(serialMessage);
  Serial.flush();

  // Incrémente l'index et boucle sur le tableau si nécessaire
  index++;
  if (index >= 100) index = 0;
}
