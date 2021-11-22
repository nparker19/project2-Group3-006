from datetime import timedelta, datetime, time


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

        initialTime = datetime.strptime("8:00 AM", "%I:%M %p")

        for i in range(0, len(timeStartList)):
            time_difference = timeStartList[i] - initialTime
            for item in suggestDict:
                t = datetime.strptime(item["duration"], "%I:%M")
                delta = timedelta(hours=t.hour + 1, minutes=t.minute)
                if time_difference > delta:
                    suggest = item["suggestion"]
                    start = initialTime.time().strftime("%I:%M %p")
                    end = timeStartList[i].time().strftime("%I:%M %p")

                    startSuggest = initialTime + timedelta(minutes=30)
                    endSuggest = startSuggest + timedelta(
                        hours=t.hour, minutes=t.minute
                    )
                    stringStartSuggest = startSuggest.time().strftime("%I:%M %p")
                    stringEndSuggest = endSuggest.time().strftime("%I:%M %p")
                    suggestList.append(
                        f"You have enough time to {suggest} between {start} and {end}. Would you like to {suggest} from {stringStartSuggest} to {stringEndSuggest} today?"
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


if __name__ == "__main__":
    scheduleDict = sortDictTimeMilitary(
        scheduleDict=[
            {"event": "class1", "startTime": "15:45", "endTime": "17:00"},
            {"event": "meeting1", "startTime": "10:00", "endTime": "11:00"},
            {"event": "group meeting", "startTime": "22:30", "endTime": "23:00"},
        ]
    )
    ans = suggest(
        scheduleDict,
        suggestDict=[
            {"suggestion": "workout", "duration": "02:00"},
            {"suggestion": "study", "duration": "03:45"},
        ],
        militaryTime=True,
    )

    print(ans)
