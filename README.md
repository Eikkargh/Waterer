# Waterer
<h>Automatic Plant Water</h> 

An automatic plant waterer based on Pi Pico W in MicroPython wired, to a moisture sensor and water pump via a relay.

<h1>Wiring</h1> 
- Moisture Sensor pin 6 (ADC)
- Pump pin 26 
 
<h1>Coding for Pico W in MicroPython</h1>
- boot.py
- main.py
  - uses umqttsimple.py from https://github.com/RuiSantosdotme/ESP-MicroPython/blob/master/code/MQTT/umqttsimple.py
- secrets.py

<h1>Home Assistant yaml snippets:</h1>
<img src="HASS Waterer.png">
- configuration.yaml
  - uses mqtt integration
- lovelace.yaml
  - lovelace.yaml is no longer used. Code should be copied into the Edit Dashboard - Raw Configuration Editor from the the lovelace menu.
  - uses card-mod integration found in HACS Frontend

