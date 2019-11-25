#!/usr/bin/env python
import json
import RPi.GPIO as GPIO
import time
import logging
from logging.handlers import TimedRotatingFileHandler

import utils
import xDoor

def main():
    print("Doorman v 0.1")
    
    # Read Config
    config = utils.readConfig()
    
    # logging config

    logging.basicConfig(format=config['logFormat'], datefmt=config['dateFormat'], level=eval(config['logLevelConsole']))
    
    logger = logging.getLogger("__xDoormanLogger__")
    handler = TimedRotatingFileHandler("logs/xDoorman.log", when="midnight", interval=1)
    handler.suffix = "%Y%m%d"
    handler.setLevel(eval(config['logLevelFile']))
    formatter = logging.Formatter(config['logFormat'])
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info("xDoorman started")
    # GPIO settings
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    
    
    lastInput = 0
    lastMovement = time.time()
    logger.debug('INPUT LOW')
    while True:
        if GPIO.input(24) == 0 and lastInput != 0:
            logger.debug('INPUT LOW')
            
        elif GPIO.input(24) == 1:# and lastInput != 1:
            logger.debug("INPUT HIGH")
            lastMovement = time.time()
            
        # xDoor.closeDoor(config)
        currentTimestamp = time.time()
        timeDiff = currentTimestamp - lastMovement
        logger.debug("TimeDiff: " + str(timeDiff))
        if timeDiff > config["delay"]:
            xDoor.closeDoor(config)
            print("close Door")
            doorStatusAfterClosing = xDoor.getDoorStatus(config)
            if doorStatusAfterClosing["hasError"] == False and doorStatusAfterClosing["status"] == False:
                # Reset Timer
                lastMovement = time.time()
            else:
                logger.error("Door not closed. Timer not reseted. (Try again in next loop iteration)")
            
        else:
            logger.debug("TimeDiff has not exceeded delay. TimeDiff: " + str(timeDiff) + " Delay: " + str(config["delay"]))
            
        lastInput = GPIO.input(24)
        time.sleep(0.5)
        
        

try:
    main()
except KeyboardInterrupt:
    pass
finally:
    logging.info("xDoorman Cleanup")
    GPIO.cleanup()


