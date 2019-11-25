import json
import logging

logger = logging.getLogger("__xDoormanLogger__")
    
def readConfig(): 
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config
