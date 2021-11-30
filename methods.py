from datetime import timedelta, datetime


def suggest(scheduleDict, suggestDict):

    """
    A function which takes in a schedule list with times (in chronological order as a string),
    and a list of items not currently in the schedule along with their durations.
    It outputs a list of suggestions on where to fit the items into the current schedule.
    This function assumes the user starts their day at 8:00 am and ends it at 11:59PM
    Time Complexity: O(N*M)
    Here N is the amount of items in the input schedule, and M is the amount of items in the suggestions input list
    It is worth noting, a user can only physically input a limited amount of tasks for a day. So let's say they
    input a task for each minute of the day (very unrealistic but still). This is the highest frequency of events they could enter
    into the app. Therefore the max schedule length will be 1,440. The user can still input infinitely many items into the suggestions
    list theoretically. With this logic we can assume that the time complexity is O(M).
    """
    timeStartList = []
    timeEndList = []
    eventList = []
    suggestList = []

    if len(scheduleDict) != 0:

        for item in scheduleDict:
            task_start_time = datetime.strptime(item["startTime"], "%I:%M %p")
            task_end_time = datetime.strptime(item["endTime"], "%I:%M %p")
            timeStartList.append(task_start_time)
            timeEndList.append(task_end_time)
            eventList.append(item["event"])

        initialTime = datetime.strptime("8:00 AM", "%I:%M %p")

        scheduleLength = len(timeStartList)

        for i in range(scheduleLength + 1):
            if i == len(timeStartList):
                floorTime = datetime.strptime("11:59 PM", "%I:%M %p")
            else:
                floorTime = timeStartList[i]

            time_difference = floorTime - initialTime

            for item in suggestDict:
                try:
                    suggestDuration = datetime.strptime(
                        item["duration"], "%I hour(s) %M minute(s)"
                    )
                    hourCatch = suggestDuration.hour
                except:
                    suggestDuration = datetime.strptime(
                        item["duration"], "0 hour(s) %M minute(s)"
                    )
                    hourCatch = 0
                # delta is time differance needed to fit the suggestion into the current Schedule. It allows for a one hour buffer
                delta = timedelta(hours=hourCatch + 1, minutes=suggestDuration.minute)
                if time_difference > delta:
                    suggest = item["suggestion"]
                    start = initialTime.time().strftime("%I:%M %p")
                    end = floorTime.time().strftime("%I:%M %p")

                    startSuggest = initialTime + timedelta(minutes=30)
                    endSuggest = startSuggest + timedelta(
                        hours=hourCatch, minutes=suggestDuration.minute
                    )
                    stringStartSuggest = startSuggest.time().strftime("%I:%M %p")
                    stringEndSuggest = endSuggest.time().strftime("%I:%M %p")
                    suggestList.append(
                        {
                            "suggestStartTime": stringStartSuggest,
                            "suggestEndTime": stringEndSuggest,
                            "suggestEvent": suggest,
                            "suggestion": f"You have enough time to {suggest} between {start} and {end}. Would you like to {suggest} from {stringStartSuggest} to {stringEndSuggest} today? (click OK to add to schedule, and click cancel to view any other suggestions)",
                        }
                    )
            # If all schedule events have been inspected then the loop exists
            if i == scheduleLength:
                break
            else:
                initialTime = timeEndList[i]

    return suggestList


def sortDictTimeRegular(scheduleDict):
    """
    This function sorts the input schedule dictionary in chronological order when events
    are in regular 12 hour time format.
    """
    if len(scheduleDict) != 0:
        scheduleDict = sorted(
            scheduleDict, key=lambda x: datetime.strptime(x["startTime"], "%I:%M %p")
        )
    return scheduleDict


def convertScheduleToRegTime(scheduleDict):

    """
    This function converts a dictionary with both 12hr (ie 10:00 AM) and 24 hr (23:00, 1:00) time formats
    to the same 12 hour format.
    Time Complexity: O(N) where N is the amount of events in the input Schedule dictionary
    Technically the user can input a max of 1,440 events into the schedule so using this logic
    the time complexity is O(1)
    """
    convertedDict = []
    for item in scheduleDict:
        try:
            itemStart = datetime.strptime(item["startTime"], "%I:%M %p")
            itemEnd = datetime.strptime(item["endTime"], "%I:%M %p")
            convertedItemStart = itemStart.strftime("%I:%M %p")
            convertedItemEnd = itemEnd.strftime("%I:%M %p")
            convertedDict.append(
                {
                    "event": item["event"],
                    "startTime": convertedItemStart,
                    "endTime": convertedItemEnd,
                }
            )
        except ValueError:
            itemStart = datetime.strptime(item["startTime"], "%H:%M")
            itemEnd = datetime.strptime(item["endTime"], "%H:%M")
            convertedItemStart = itemStart.strftime("%I:%M %p")
            convertedItemEnd = itemEnd.strftime("%I:%M %p")
            convertedDict.append(
                {
                    "event": item["event"],
                    "startTime": convertedItemStart,
                    "endTime": convertedItemEnd,
                }
            )
    return convertedDict
