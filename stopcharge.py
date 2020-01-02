from time import sleep
import logging

import requests
import androidhelper

charge_limit = 80 #percent
sonoff_device_id = "PUT_ID_HERE" #deviceId of the switch charger is plugged into
sonoff_ip = 'PUT_SWITCH_IP_HERE' #or, lookup via mDNS
wait_delay = 15 #seconds

stop_url = 'http://{}:8081/zeroconf/switch'.format(sonoff_ip)
logger = logging.getLogger(__name__)
def stop_charge():
    print('Turning smart switch: off')
    try:
        requests.post(stop_url,json={"deviceId": sonoff_device_id,"data":{"switch":"off"}})
    except requests.exceptions.ConnectionError:
        logger.error('ConnectionError')

droid = androidhelper.Android()
droid.batteryStartMonitoring()

droid.eventWaitFor('battery')
while True:
    if droid.batteryGetPlugType().result > 0: #any Charging type
        if droid.batteryGetLevel().result >= charge_limit:
            stop_charge()
    sleep(wait_delay)