# Simple module to call REST API when Android device charges to target battery %
#
# Copyright (C) 2020 Brandon J. Van Vaerenbergh

from time import sleep
import logging
import os
from pprint import pformat

import requests
import androidhelper
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils import unicode_paths

config_path = "config.yml"
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

config = {} #load from path & reload on file change
stop_url = ''
module_dir = os.path.dirname(os.path.abspath(__file__))
config_abspath = os.path.join(module_dir, config_path)

def get_config():
    global config, stop_url
    logger.info("Loading "+config_path)
    with open(config_abspath) as yml:
        config = yaml.safe_load(yml)
    stop_url = 'http://{}:8081/zeroconf/switch'.format(config["sonoff"]["ip"])
    logger.debug("Values "+pformat(config))

class ConfigHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and unicode_paths.decode(event.src_path) == config_abspath:
            get_config()

get_config()
config_reloader = Observer()
config_reloader.schedule(ConfigHandler(), module_dir)
config_reloader.start()

def stop_charge():
    logger.info('Turning smart switch: off')
    try:
        requests.post(stop_url,json={"deviceId": config["sonoff"]["device_id"],"data":{"switch":"off"}})
    except requests.exceptions.ConnectionError:
        logger.error('ConnectionError')

try:
    droid = androidhelper.Android()
except ConnectionRefusedError as e:
    raise RuntimeError("SL4A Service unreachable") from e
droid.batteryStartMonitoring()

droid.eventWaitFor('battery')
while True:
    if droid.batteryGetPlugType().result > 0: #any Charging type
        if droid.batteryGetLevel().result >= config["charge_limit"]:
            stop_charge()
    sleep(config["wait_delay"])
