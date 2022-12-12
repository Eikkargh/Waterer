# Waterer
<h>Automatic Plant Water</h> 

An automatic plant waterer based on Pi Pico W in MicroPython wired, to a moisture sensor and water pump via a relay.

<h2>Wiring</h2> 
<ul>
    <li>Moisture Sensor pin 6 (ADC)</li>
    <li>Pump pin 26</li>
</ul>
 
<h2>Coding for Pico W in MicroPython</h2>
<ul>
  <li>boot.py</li>
  <li>main.py</li>
    <ul><li>uses umqttsimple.py from https://github.com/RuiSantosdotme/ESP-MicroPython/blob/master/code/MQTT/umqttsimple.py</li></ul>
  <li>secrets.py</li>
<ul>
  
<h2>Home Assistant yaml</h2>
<img src="HASS Waterer.png">
<ul>
    <li>configuration.yaml</li>
    <ul><li>uses mqtt integration</li></ul>
    <li>lovelace.yaml</li>
    <ul><li>lovelace.yaml is no longer used. Code should be copied into the Edit Dashboard - Raw Configuration Editor from the the lovelace menu.</li>
    <li>uses card-mod integration found in HACS Frontend</li>
 </ul>
