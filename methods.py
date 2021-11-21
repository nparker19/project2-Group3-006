from datetime import datetime, timedelta

"""
    A function which takes in a schedule list with times (in chronological order as a string),
    a list of items not currently in the schedule along with their durations, and a boolean value which keeps track of time formatting.
    It outputs a list of suggestions on where to fit the items not currently in the schedule.
"""


def suggest(scheduleDict, suggestDict, militaryTime):
    timeStartList = []
    timeEndList = []
    eventList = []
    suggestList = []

    if len(scheduleDict) != 0:
        for item in scheduleDict:
            if militaryTime:
                task_start_time = datetime.strptime(item["startTime"], "%H:%M")
                task_end_time = datetime.strptime(item["endTime"], "%H:%M")
            elif not militaryTime:
                task_start_time = datetime.strptime(item["startTime"], "%I:%M %p")
                task_end_time = datetime.strptime(item["endTime"], "%I:%M %p")
            timeStartList.append(task_start_time)
            timeEndList.append(task_end_time)
            eventList.append(item["event"])

        initialTime = timeEndList[0]
        for i in range(1, len(timeStartList)):
            time_difference = timeStartList[i] - initialTime
            for item in suggestDict:
                t = datetime.strptime(item["duration"], "%I:%M")
                delta = timedelta(hours=t.hour + 1, minutes=t.minute)
                if time_difference > delta:
                    suggest = item["suggestion"]
                    start = initialTime.time().strftime("%I:%M %p")
                    end = timeStartList[i].time().strftime("%I:%M %p")

                    suggestList.append(
                        f"You have enough time to {suggest} between {start} and {end} today "
                    )
            initialTime = timeEndList[i]
    return suggestList


# This function sorts the schedule dictionary in chronological order when events are in military time
def sortDictTimeMilitary(scheduleDict):
    if len(scheduleDict) != 0:
        scheduleDict = sorted(
            scheduleDict, key=lambda x: datetime.strptime(x["startTime"], "%H:%M")
        )
    return scheduleDict


# This function sorts the schedule dictionary in chronological order when events are in regular 12 hour time
def sortDictTimeRegular(scheduleDict):
    if len(scheduleDict) != 0:
        scheduleDict = sorted(
            scheduleDict, key=lambda x: datetime.strptime(x["startTime"], "%I:%M %p")
        )
    return scheduleDict
