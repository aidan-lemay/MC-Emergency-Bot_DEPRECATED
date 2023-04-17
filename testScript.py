from datetime import datetime, timedelta
import time
import requests
from typing import Optional

ems = "https://cc.k9fgt.me/api/v1/calls?system=us.ny.monroe&talkgroup=1077"
henfire = "https://cc.k9fgt.me/api/v1/calls?system=us.ny.monroe&talkgroup=1654"
pub = "https://cc.k9fgt.me/api/v1/calls?system=us.ny.monroe&talkgroup=3070"

def get_source_clearcut(url):
    try:
        data = requests.get(url=url)
        response = data.json()
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_feed_ems(num: Optional[int], keyword: Optional[str]):
    response = get_source_clearcut(ems)
    fSize = len(response)
    seconds = time.time()
    message = "```Monroe County EMS Call Transcripts:\n"

    for data in response:
        curtime = datetime.today()
        timestamp = datetime.fromtimestamp(data['startTime'])
        calltime = datetime.fromtimestamp(data['startTime'])
        mintime = curtime - timedelta(hours = 24)
        text = data['transcript']['text']

        if (num > 0 & num < 24):
            mintime = curtime - timedelta(hours = num)
        elif (num > 24):
            mintime = curtime - timedelta(hours = 24)

        if (keyword is not None):
            # Get all calls within num range with matching keywords
            if (calltime > mintime and keyword in text):
                message += str(timestamp) + " | " + text + "\n"
        else:
            # Get all calls within num range
            if (calltime > mintime):
                message += str(timestamp) + " | " + text + "\n"

    message += "```"
        
    print(message)


get_feed_ems(1, "RIT")