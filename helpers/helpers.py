import time
import random
import os
import datetime

def think(min_wait_sec, max_wait_sec):
    if "SKIP_THINK" in os.environ:
        return

    time.sleep(random.uniform(min_wait_sec, max_wait_sec))

def maybe():
    return random.choice([True, False])

#Based on the day of week and time of day return a probability based boolean indicating whether or not
#the run should abort to simulate reduced load against the system
def shouldIAbort():
    #list item 0 is monday, 6 is sunday
    dayOfWeekProbability = [0.9, 0.9, 0.85, 0.8, 0.8, 0.3, 0.3]
    #list item 0 is hour 0, 23 is hour 23
    hourOfDayProbability = [0.1, 0.1, 0.1, 0.1, 0.1, 0.15, 0.4, 0.6, 0.9, 0.9, 0.9, 0.9,
                            0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.8, 0.4, 0.4, 0.2, 0.2, 0.1]

    dayOfWeek = datetime.datetime.today().weekday()
    if random.uniform(0, 1) > dayOfWeekProbability[dayOfWeek]:
        return True

    hourOfDay = datetime.datetime.today().hour
    if random.uniform(0, 1) > hourOfDayProbability[hourOfDay]:
        return True
    
    return False

def getProbabilityCount(max_count):
    actual_count = 0
    for i in range(0, max_count):
        if (not shouldIAbort()): actual_count+=1

    return actual_count

def weightedChoice(choice_weight_list):
    total = sum(w for c, w in choice_weight_list)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choice_weight_list:
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"