import time
import random
import os
import datetime

def think(min_wait_sec, max_wait_sec):
    if "SKIP THINK" in os.environ:
        return

    time.sleep(random.uniform(min_wait_sec, max_wait_sec))

def maybe():
    return random.choice([True, False])

#Based on the day of week and time of day return a probability based boolean indicating whether or not
#the run should abort to simulate reduced load against the system
def shouldIAbort():
    dayOfWeekProbability = {0:0.9, 1:0.9, 2:0.85, 3:0.8, 4:0.8, 5:0.3, 6:0.3}
    hourOfDayProbability = {0:0.1, 1:0.1, 2:0.1, 3:0.1, 4:0.1, 5:0.15, 6:0.4,
                            7:0.6, 8:0.9, 9:0.9, 10:0.9, 11:0.9, 12:0.9, 13:0.9,
                            14:0.9, 15:0.9, 16:0.9, 17:0.9, 18:0.8, 19:0.4,
                            20:0.4, 21:0.2, 22:0.2, 23:0.1}

    dayOfWeek = datetime.datetime.today().weekday()
    if random.uniform(0, 1) > dayOfWeekProbability[dayOfWeek]:
        return True

    hourOfDay = datetime.datetime.today().hour
    if random.uniform(0, 1) > hourOfDayProbability[hourOfDay]:
        return True
    
    return False