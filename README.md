# Waterer
Automatic Plant Water

An automatic plant waterer based on Pi Pico W in MicroPython wired to a moisture sensor and water pump.

Moisture Sensor pin 6 (ADC)
Pump pin 26 

Home Assistant yaml snippets:
- configuration.yaml


lovelace.yaml
Note lovelace.yaml is no longer used. Code should be copied into the Edit Dashboard - Raw Configuration Editor from the the lovelace menu.

This uses umqttsimple.py from https://github.com/RuiSantosdotme/ESP-MicroPython/blob/master/code/MQTT/umqttsimple.py
