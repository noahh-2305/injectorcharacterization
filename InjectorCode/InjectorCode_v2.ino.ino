int pins[4] = {5, 6, 7, 8}; // pins
float duty_cycles[4] = {0.6, 0.6, 0.6, 0.6};
float periods[4]     = {250,250,250,250}; // milliseconds
float offsets[4]     = {0.0, 0.25, 0.50, 0.75}; // (0 to .999999)

unsigned int total_cycles = 10; // total sequences (injector fires)
unsigned int currentCycle = 0;
unsigned long InjStart = 0;

void setup() { // set all pins to output mode and low (off) initially
  for (int i = 0; i < 4; i++) pinMode(pins[i], OUTPUT);
  for (int i = 0; i < 4; i++) digitalWrite(pins[i], LOW);
  InjStart = millis();
}

void loop() { // make sure each pin is off after cycle threshold is reached
  if (currentCycle >= total_cycles) {
    for (int i = 0; i < 4; i++) digitalWrite(pins[i], LOW);
    return;
  }

  unsigned long now = millis();

  
  unsigned long InjDuration = 0;
  for (int i = 0; i < 4; i++) {
    unsigned long currentInjEnd = (unsigned long)(periods[i] * offsets[i]) + (periods[i] * duty_cycles[i]);
    if (currentInjEnd > InjDuration) InjDuration = currentInjEnd;
  }


  unsigned long elapsed = now - InjStart;

  // Calculate how long each injector is on for, when it starts and when it ends relative to other injectors
  for (int i = 0; i < 4; i++) {
    unsigned long onTime  = periods[i] * duty_cycles[i];
    unsigned long start   = InjStart + (unsigned long)(periods[i] * offsets[i]);
    unsigned long end     = start + onTime;

    // on and off settings
    if (now >= start && now < end) {
      digitalWrite(pins[i], HIGH);
    } else {
      digitalWrite(pins[i], LOW);
    }
  }

  // Check if this sequence finished
  if (elapsed >= InjDuration) {
    currentCycle++;
    InjStart = now; // reset for next cycle
  }
}
