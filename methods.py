from datetime import datetime, timedelta

# A function which takes in a list of times (as a string), and outputs schedule suggestions
def suggest(scheduleDict):
    timeList = []
    eventList = []
    suggestList = []
    for item in scheduleDict:
        task_time = datetime.strptime(item["time"], "%I:%M %p")
        timeList.append(task_time)
        eventList.append(item["event"])

    if len(timeList) != 0:
        initialTime = timeList[0]
        for i in range(1, len(timeList)):
            time_difference = timeList[i] - initialTime
            if time_difference >= timedelta(hours=10):
                suggestList.append(
                    "You have a large amount of time between "
                    + eventList[i - 1]
                    + " and "
                    + eventList[i]
                    + ". Plenty of time to work out, or run errands"
                )
            if time_difference >= timedelta(hours=6) and time_difference < timedelta(
                hours=10
            ):
                suggestList.append(
                    "You have a good amount of time between "
                    + eventList[i - 1]
                    + " and "
                    + eventList[i]
                    + " You could get in a workout and a study session. "
                )
            if time_difference >= timedelta(hours=3) and time_difference < timedelta(
                hours=6
            ):
                suggestList.append(
                    "You have some time between "
                    + eventList[i - 1]
                    + " and "
                    + eventList[i]
                    + ". This would be a great time to study or get in quick nap."
                )
            initialTime = timeList[i]
    return suggestList
