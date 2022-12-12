# Waterer
<b>Automatic Plant Water</b>
An automatic plant waterer based on Pi Pico W in MicroPython wired, to a moisture sensor and water pump via a relay.

<b>Wiring</b>
Moisture Sensor pin 6 (ADC)
Pump pin 26 
    
<b>Coding for Pico W in MicroPython</b>
- boot.py
- main.py
  - uses umqttsimple.py from https://github.com/RuiSantosdotme/ESP-MicroPython/blob/master/code/MQTT/umqttsimple.py
- secrets.py
  
<b>Home Assistant yaml snippets:</b>
- configuration.yaml
  - uses mqtt integration
- lovelace.yaml
  - lovelace.yaml is no longer used. Code should be copied into the Edit Dashboard - Raw Configuration Editor from the the lovelace menu.
  - uses card-mod integration found in HACS Frontend

