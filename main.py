from machine import ADC, Pin
from umqttsimple import MQTTClient
import time
import secrets
import _thread
import json

#system settings
boot = time.time()
reboot_days = 1 #0 is infinite else days

#MQTT Client settings
client_id = 'Waterer'
mqtt_server = secrets.MQTT
topic_pump = b'waterer/waterpump'
topic_config = b'waterer/config'
topic_restart = b'waterer/restart'
topic_moist = b'waterer/moisture'
topic_status = b'waterer/status'

#Moisture sensor settings
soil = ADC(Pin(26))
min_moisture = 48200
max_moisture = 18000
last_message = 0
message_interval = 60
max_threshold = 50
min_threshold = 10
last_state = b'loading'

#Pump settings
pump = Pin(6, Pin.OUT)
max_water_cycles = 6
pump_on_time = 3
pump_interval = 10
pump_req = 'None'
lock = _thread.allocate_lock()

def calibrate():
    global min_moisture, max_moisture, message_interval, max_threshold, min_threshold, max_water_cycles, pump_on_time, pump_interval
    settings = config.get('settings')
    min_moisture = settings.get('min_moisture')
    max_moisture = settings.get('max_moisture')
    message_interval = settings.get('message_interval')
    max_threshold = settings.get('max_threshold')
    min_threshold = settings.get('min_threshold')
    max_water_cycles = settings.get('max_water_cycles')
    pump_on_time = settings.get('pump_on_time')
    pump_interval = settings.get('pump_interval')
    reboot_days = settings.get('reboot_days')
    config.update({'settings': settings})
    config.update({'calibrate': 'False'})
    config_json = json.dumps(config)
    client.publish(topic_config, config_json, retain=True)
    
def run_pump():
    global pump_req
    client.publish(topic_pump, b'Pumping')
    count = 0
    while moisture < max_threshold:
        if pump_req == b'Cancel':
            return
        count += 1
        pump(1)
        time.sleep(pump_on_time)
        pump(0)
        print('pump requested: %s Cycles: %s' % (pump_req, count))
        time.sleep(pump_interval)
        if count >= max_water_cycles:
            print('Low water. Please check level')
            client.publish(topic_pump, b'Low Water')
    lock.acquire()
    pump_req = 'None'
    lock.release()            
    print('Pump request complete after %s cycles.' % count)
    client.publish(topic_pump, b'Complete') 
    client.publish(topic_moist, '%.1f' % moisture, retain=True)

def sub_cb(topic, msg):
    global pump_req, config
    print(topic, msg)
    if topic == b'waterer/config':
        config = json.loads(msg)
        if config['calibrate'] == 'True':
            lock.acquire()
            calibrate()
            lock.release()
            print('Calibration complete')
    if topic == b'waterer/waterpump':
        if msg == b'Cancelled':
            lock.acquire()
            pump_req = 'Cancel'
            lock.release()
        if msg == b'Requested' and pump_req != 'Active':
            lock.acquire()
            pump_req = 'Manual'
            lock.release()
        if msg == b'Complete' or msg == b'Cancelled':
            time.sleep(60)
            client.publish(topic_pump, b'Available', retain=True)
    if topic == b'waterer/restart' and msg == b'Reboot':
        restart()
        
def mqtt_connect():
    global client_id, mqtt_server, topic_sub_pump
    client = MQTTClient(client_id,mqtt_server, keepalive=3600)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_pump)
    client.subscribe(topic_config)
    client.subscribe(topic_restart)
    client.publish(topic_restart, b'Loaded', retain=True)
    client.publish(topic_pump, b'Available', retain=True)
    print('MQTT connected. Broker: %s' % mqtt_server)
    return client

def restart():
    lock.acquire()
    pump_req = 'Cancel'
    lock.release()
    print("Restarting in 30 seconds.")
    client.publish(topic_pump, b'Rebooting', retain=True)
    time.sleep(30)
    machine.reset()

#connect to MQTT Broker 
try:
    client = mqtt_connect()
    client.publish(topic_restart, b'Loaded')
except OSError as e:
    print('Failed to connect to MQTT broker. Reconnecting...')
    client.publish(topic_pump, b'Connect Error')
    restart()

while True:
#check for pump requests
    try:
        client.check_msg()
        if pump_req == "Manual":
            print('manual req triggered.')
            second_thread = _thread.start_new_thread(run_pump, ())
    except:
        print('failed to get pump status from MQTT')
        client.publish(topic_pump, b'MQTT Error')
        restart()
        
#read moisture value
    try:
        moisture = 100-(max_moisture-soil.read_u16())*100/(max_moisture-min_moisture)
        if (time.time() - last_message) > message_interval:
            client.publish(topic_moist, '%.1f' % moisture)         
            last_message = time.time()  
            if moisture < min_threshold:
                last_state = b'Dry'
                lock.acquire()
                pump_req = 'Auto'
                lock.release()
            elif moisture < max_threshold:
                last_state = b'Moist'
            elif last_state != b'Wet':
                last_state = b'Wet'
            client.publish(topic_status, last_state, retain=True)      
    except OSError as e:
        print('Error reading moisture')
        client.publish(topic_pump, b'Read Error')
        restart()

#Auto pump request
    try:
        if pump_req == 'Auto':
            lock.acquire()
            pump_req = 'Active'
            lock.release()
            print('Pump auto request. pump_req: %s' % pump_req)
            second_thread = _thread.start_new_thread(run_pump, ())
    except:
        print('Pump request error')
        client.publish(topic_pump, b'Pump Error')
        restart()

#scheduled restart
    if reboot_days != 0 and (time.time() - boot) > (reboot_days * 86400):
        restart()
