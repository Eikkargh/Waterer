from machine import ADC, Pin
from umqttsimple import MQTTClient
import time
import secrets
import _thread
import json

#setting up MQTT Client
client_id = "Waterer"
mqtt_server = secrets.MQTT
topic_sub_pump = b'waterer/waterpump'
topic_sub_config = b'waterer/config'
topic_pub_moist = b'waterer/moisture'
topic_pub_pump = b'waterer/waterpump'
topic_pub_status = b'waterer/status'
topic_pub_config = b'waterer/config'

#setting up moisture sensor
soil = ADC(Pin(26))
min_moisture = 48200
max_moisture = 18000
last_message = 0
message_interval = 3600
max_threshold = 80
min_threshold = 10
calibrate = False

#setting up pump
pump = Pin(6, Pin.OUT)
max_water_cycles = 4
pump_on_time = 2
pump_interval = 10
pump_req = 'None'
lock = _thread.allocate_lock()

def calibrate():
    global config
    min_moisture = config['settings']['min_moisture']
    max_moisture = config['settings']['max_moisture']
    message_interval = config['settings']['message_interval']
    max_threshold = config['settings']['max_threshold']
    min_threshold = config['settings']['min_threshold']
    max_water_cycles = config['settings']['max_water_cycles']
    pump_on_time = config['settings']['pump_on_time']
    pump_interval = config['settings']['pump_interval']
    config.update({"calibrate": False})
    config_json = json.dumps(config)
    client.publish(topic_pub_config, config_json)
    
def run_pump():
    global pump_req
    client.publish(topic_pub_pump, b'Pumping')
    count = 0
    while moisture < max_threshold:
        if pump_req == 'Cancel':
            return
        count += 1
        pump(1)
        time.sleep(pump_on_time)
        pump(0)
        print('pump requested: %s Cycles: %s' % (pump_req, count))
        time.sleep(pump_interval)
        if count >= max_water_cycles:
            print('Low water. Please check level')
            client.publish(topic_pub_pump, b'Low Water')
            lock.aquire()
            pump_req = 'None'
            lock.release()            
            return
    print('Pump request complete after %s cycles.' % count)
    client.publish(topic_pub_pump, b'Complete') 
    client.publish(topic_pub_moist, '%.1f' % moisture)
    lock.aquire()
    pump_req = 'None'
    lock.release()

def sub_cb(topic, msg):
    global pump_req, config
    print(topic, msg)
    if topic == b'waterer/config':
        config = json.loads(msg)
        if config['calibrate']:
            lock.aquire()
            calibrate()
            lock.release()
            print('Calibration complete')
    if topic == b'waterer/waterpump' and (msg == b'Cancelled'):
        lock.acquire()
        pump_req = 'Cancel'
        lock.release()
        print('Pump manually Cancelled. pump_req: %s' % pump_req)
    if topic == b'waterer/waterpump' and (msg == b'Requested'):
        lock.acquire()
        pump_req = 'Manual'
        lock.release()
        print('Pump manually Requested. pump_req: %s' % pump_req)
    if topic == b'waterer/waterpump' and (msg == b'Complete' or msg == b'Cancelled'):
        time.sleep(60)
        client.publish(topic_pub_pump, b'Available')      
        
def mqtt_connect():
    global client_id, mqtt_server, topic_sub_pump
    client = MQTTClient(client_id,mqtt_server, keepalive=3600)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub_pump)
    client.subscribe(topic_sub_config)
    print('MQTT connected. Broker: %s' % mqtt_server)
    return client

def restart():
    time.sleep(30)
    machine.reset()

#connect to MQTT Broker 
try:
    client = mqtt_connect()
except OSError as e:
    print('Failed to connect to MQTT broker. Reconnecting...')
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
        restart()
        
#read moisture value
    try:
        moisture = 100-(max_moisture-soil.read_u16())*100/(max_moisture-min_moisture)
        if (time.time() - last_message) > message_interval: #check time and publish moisture
            client.publish(topic_pub_moist, '%.1f' % moisture)         
            last_message = time.time()        
            if moisture < min_threshold:
                client.publish(topic_pub_status, b'Dry')
                if pump_req == 'None':
                    lock.acquire()
                    pump_req = 'Auto'
                    lock.release()
                    print('Pump activeated automattically. pump_req: %s' % pump_req)
                    second_thread = _thread.start_new_thread(run_pump, ())
            elif moisture < max_threshold:
                client.publish(topic_pub_status, b'Moist')
            else:
                client.publish(topic_pub_status, b'Wet')
    except OSError as e:
        print('Error reading moisture')
        restart()
