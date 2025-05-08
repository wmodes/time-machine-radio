#include <Arduino.h>

// === USER-SERVICEABLE PARTS ===
const int avgWindow = 250;                // Number of past samples to average
const float MAX_READING = 860.0f;         // Calibrated max sensor value
const float MIN_READING = 300.0f;         // Calibrated min sensor value

const bool printOnlyIfChanged = true;    // If true, print only when value changes
const bool ledBlink = true;               // If true, blink LED when value changes
// ===============================

// === CONSTANTS ===
const uint8_t OUT_PIN = A2;               // Excitation pin
const uint8_t IN_PIN = A0;                // Sensor input pin
// =================

int blink = 0;
int old = 0;

int readings[avgWindow];                  // Circular buffer for readings
int readIndex = 0;
long total = 0;
int sampleCount = 0;

int sampleInput()
{
  pinMode(IN_PIN, INPUT);
  digitalWrite(OUT_PIN, HIGH);
  int val = analogRead(IN_PIN);
  digitalWrite(OUT_PIN, LOW);
  pinMode(IN_PIN, OUTPUT);
  return val;
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(OUT_PIN, OUTPUT);
  pinMode(IN_PIN, OUTPUT);

  for (int i = 0; i < avgWindow; i++) readings[i] = 0;
}

void loop() {
  int raw = sampleInput();

  // Update circular buffer
  total -= readings[readIndex];
  readings[readIndex] = raw;
  total += raw;
  readIndex = (readIndex + 1) % avgWindow;

  if (sampleCount < avgWindow) sampleCount++;

  int average = total / sampleCount;

  if (!printOnlyIfChanged || average != old) 
  {
      Serial.print("Tune: ");
      Serial.println(average);
      old = average;

      if (ledBlink)
      {
        digitalWrite(LED_BUILTIN, blink ? HIGH : LOW);  
        blink = !blink;
      }
  }
}

