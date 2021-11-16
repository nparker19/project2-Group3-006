from datetime import datetime, timedelta

# A function which takes in a list of times (as a string), and outputs schedule suggestions
def suggest(scheduleDict):
    timeStartList = []
    timeEndList = []
    eventList = []
    suggestList = []

    # Schedule must be sorted in chronological order or the times will not be accurate
    if len(scheduleDict) != 0:
        scheduleDict = sorted(
            scheduleDict, key=lambda x: datetime.strptime(x["startTime"], "%H:%M")
        )
    for item in scheduleDict:
        task_start_time = datetime.strptime(item["startTime"], "%H:%M")
        task_end_time = datetime.strptime(item["endTime"], "%H:%M")
        timeStartList.append(task_start_time)
        timeEndList.append(task_end_time)
        eventList.append(item["event"])

    initialTime = timeEndList[0]
    for i in range(1, len(timeStartList)):
        time_difference = timeStartList[i] - initialTime
        if time_difference >= timedelta(hours=10):
            suggestList.append(
                "You have a over 9 hours of free time between "
                + eventList[i - 1]
                + " and "
                + eventList[i]
                + ". Plenty of time to work out, or run errands"
            )
        if time_difference >= timedelta(hours=6) and time_difference < timedelta(
            hours=10
        ):
            suggestList.append(
                "You have over 5 hours of free time between "
                + eventList[i - 1]
                + " and "
                + eventList[i]
                + ". You could get in a workout and a study session!"
            )
        if time_difference >= timedelta(hours=3) and time_difference < timedelta(
            hours=6
        ):
            suggestList.append(
                "You have a few hours of free time between "
                + eventList[i - 1]
                + " and "
                + eventList[i]
                + ". This would be a great time to study or get in quick nap."
            )
        initialTime = timeEndList[i]
    return suggestList


if __name__ == "__main__":
    ans = suggest(
        scheduleDict=[
            {"event": "class", "startTime": "09:00 AM", "endTime": "10:45 AM"},
            {"event": "meeting", "startTime": "06:30 PM", "endTime": "07:00 PM"},
            {"event": "meeting2", "startTime": "10:00 PM", "endTime": "11:15 PM"},
        ]
    )
    print(ans)
