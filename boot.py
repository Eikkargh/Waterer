import time
import network
import secrets

#Settings for Wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)

#wait for connection or give error
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print("Waiting to connect to wifi")
    time.sleep(1)
    
#handle errors
if wlan.status() != 3:
    raise RuntimeError("Connection failed")
else:
    status = wlan.ifconfig()
    print("Connected to wifi. IP = " + status[0] )