import logging
import json
import time
import requests
from lib.pexpect import pxssh

logger = logging.getLogger("__xDoormanLogger__")
    
def closeDoor(config):
    logger.info("Closing xDoor")
    doorStatus = getDoorStatus(config)
    s = pxssh.pxssh()
    if doorStatus["status"]:
        try:
            if not s.login(config["hostname"], config["username"], ssh_key=config["pathToPrivateKey"], sync_multiplier=3, auto_prompt_reset=False): #, sync_multiplier=3, auto_prompt_reset=False
                logging.error("SSH session failed.", s)
                print (str(s))
            else:      
                logging.debug("SSH session opened")
                logger.info("xDoor closed")
                s.sendline ('ls -l')
                s.prompt()         # match the prompt
                print (s.before)   # print everything before the prompt.
                s.logout()
                logging.debug("SSH Session closed")
                # Wait for door closing
                time.sleep(30)
        except Exception as e:
            logger.error("Error With SSH Connection. Message: " + e.message, )
    else:
        logger.info("Door is already closed")
        
def getDoorStatus(config): 
    #with open('xDoorMock.json', 'r') as f:
    #    doorStatus = json.load(f)
    logger.debug("getDoorStatus")
    result = dict()
    url = config["doorStatusUrl"]
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result['hasError'] = False
        result['status']   = json.loads(response.text)["status"]
        logger.info("Door State (true = open; false = closed): " + str(result['status']))
        return result
    else:
        handleDoorStateError();
        result['hasError'] = True
        result['status']   = false
        return result 

def handleDoorStateError(config, response):
    logging.error("Error retrieving door state", response)

#def isDoorClosed(config):
#    doorStatus = getDoorStatus(config)
#    return not doorStatus["status"];
    
#def isDoorOpen(config):
#    doorStatus = getDoorStatus(config)
#    return doorStatus["status"];

    
