# Automatic Plant Water

An automatic plant waterer based on Pi Pico W in MicroPython wired, to a moisture sensor and water pump via a relay.

<h2>Wiring</h2> 
<ul>
    <li>Moisture Sensor pin 6 (ADC)</li>
    <li>Pump pin 26</li>
</ul>
 
<h2>Coding for Pico W in MicroPython</h2>
<ul>
  <li>micropython.uf2 for PicoW from: <a href=https://www.raspberrypi.com/documentation/microcontrollers/micropython.html>Rapsberry Pi Documentation</a></li>
  <li>boot.py</li>
  <li>main.py</li>
    <ul><li>uses umqttsimple.py from: <a href=https://github.com/RuiSantosdotme/ESP-MicroPython/blob/master/code/MQTT/umqttsimple.py>GitHub:RuiSantosdotme</a></li></ul>
  <li>secrets.py</li>
  <li>config.json</li>
    <ul><li>Stores last config between reboots</li>
    <li>Replace with this if setting config in Home Assistant breaks</li></ul>
</ul>
  
<h2>Home Assistant yaml</h2>
<img src="HASS Waterer.png">
<ul>
    <li>configuration.yaml</li>
    <ul>
        <li>uses mqtt integration</li>
    </ul>
    <li>lovelace.yaml</li>
    <ul>
        <li>lovelace.yaml is no longer used. Code should be copied into the Edit Dashboard - Raw Configuration Editor from the the lovelace menu.</li>
    </ul>
</ul>
