# Waterer
<h>Automatic Plant Water</h> 

An automatic plant waterer based on Pi Pico W in MicroPython wired, to a moisture sensor and water pump via a relay.

<h2>Wiring</h2> 
- Moisture Sensor pin 6 (ADC)
- Pump pin 26 
 
<h2>Coding for Pico W in MicroPython</h2>
- boot.py
- main.py
  - uses umqttsimple.py from https://github.com/RuiSantosdotme/ESP-MicroPython/blob/master/code/MQTT/umqttsimple.py
- secrets.py

<h2>Home Assistant yaml</h2>
<img src="HASS Waterer.png">
- configuration.yaml
  - uses mqtt integration
- lovelace.yaml
  - lovelace.yaml is no longer used. Code should be copied into the Edit Dashboard - Raw Configuration Editor from the the lovelace menu.
  - uses card-mod integration found in HACS Frontend

