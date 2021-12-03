# pylint: disable=C0330
"""
This python file includes server side functions which help to provide
schedule suggestions to the client.
"""
from datetime import timedelta, datetime


def suggest_generator(schedule_dict, suggest_dict):

    """
    A function which takes in a schedule list with times (in chronological order
    AND in 12 hour format, as a string),and a list of items not currently in the
    schedule along with their durations.It outputs a list of suggestions on where
    to fit the itemsinto the current schedule.This function assumes the user starts
    their day at 8:00 am and ends it at 11:59PM

    Time Complexity: O(N*M)
    Here N is the amount of items in the input schedule, and M is the amount of
    items in the suggestions input list. It is worth noting, a user can only physically
    input a limited amount of tasks for a day. So let's say they input a task for each
    minute of the day (very unrealistic but still). This is the highest frequency of events
    they could enter into the app. Therefore the max schedule length will be 1,440. The user
    can still input infinitely many items into the suggestions list theoretically. With this
    logic we can assume that the time complexity is O(M).
    """
    time_start_list = []
    time_end_list = []
    suggest_list = []

    if len(schedule_dict) != 0:
        # Stripping the times in datetime format to make code easier to read
        for item in schedule_dict:
            time_start_list.append(datetime.strptime(item["startTime"], "%I:%M %p"))
            time_end_list.append(datetime.strptime(item["endTime"], "%I:%M %p"))

        initial_time = datetime.strptime("8:00 AM", "%I:%M %p")

        for i in range(len(time_start_list) + 1):
            if i == len(time_start_list):
                floor_time = datetime.strptime("11:59 PM", "%I:%M %p")
            else:
                floor_time = time_start_list[i]

            time_difference = floor_time - initial_time

            for item in suggest_dict:

                suggest_duration = datetime.strptime(
                    item["duration"], "%H hour(s) %M minute(s)"
                )

                # time differance needs to be greater than the event duration plus one hour
                if time_difference > timedelta(
                    hours=suggest_duration.hour + 1, minutes=suggest_duration.minute
                ):
                    start = initial_time.time().strftime("%I:%M %p")
                    end = floor_time.time().strftime("%I:%M %p")

                    string_start_suggest = (
                        (initial_time + timedelta(minutes=30))
                        .time()
                        .strftime("%I:%M %p")
                    )
                    string_end_suggest = (
                        (
                            initial_time
                            + timedelta(minutes=30)
                            + timedelta(
                                hours=suggest_duration.hour,
                                minutes=suggest_duration.minute,
                            )
                        )
                        .time()
                        .strftime("%I:%M %p")
                    )
                    suggest_list.append(
                        {
                            "suggestStartTime": string_start_suggest,
                            "suggestEndTime": string_end_suggest,
                            "suggestEvent": item["suggestion"],
                            "suggestion": "You have enough time to "
                            + item["suggestion"]
                            + " between "
                            + start
                            + " and "
                            + end
                            + ". Would you like to "
                            + item["suggestion"]
                            + " from "
                            + string_start_suggest
                            + " to "
                            + string_end_suggest
                            + " today? (click OK to add, and click cancel to see more suggestions)",
                        }
                    )
            # If all schedule events have been inspected then the loop exists
            if i == len(time_start_list):
                break

            initial_time = time_end_list[i]

    return suggest_list


def sort_dict_time_regular(schedule_dict):
    """
    This function sorts the input schedule dictionary in chronological
    order when events are in regular 12 hour time format.
    """
    if len(schedule_dict) != 0:
        schedule_dict = sorted(
            schedule_dict, key=lambda x: datetime.strptime(x["startTime"], "%I:%M %p")
        )
    return schedule_dict


def convert_schedule_to_reg_time(schedule_dict):

    """
    This function converts a dictionary with both 12hr (ie 10:00 AM) and 24 hr (23:00, 1:00)
    time formats to the same 12 hour format.

    Time Complexity: O(N) where N is the amount of events in the input Schedule dictionary
    Technically the user can input a max of 1,440 events into the schedule so using this logic
    the time complexity is O(1)
    """
    converted_dict = []
    for item in schedule_dict:
        try:
            converted_item_start = datetime.strptime(
                item["startTime"], "%I:%M %p"
            ).strftime("%I:%M %p")
            converted_item_end = datetime.strptime(
                item["endTime"], "%I:%M %p"
            ).strftime("%I:%M %p")
            converted_dict.append(
                {
                    "event": item["event"],
                    "startTime": converted_item_start,
                    "endTime": converted_item_end,
                }
            )
        except ValueError:
            converted_item_start = datetime.strptime(
                item["startTime"], "%H:%M"
            ).strftime("%I:%M %p")
            converted_item_end = datetime.strptime(item["endTime"], "%H:%M").strftime(
                "%I:%M %p"
            )
            converted_dict.append(
                {
                    "event": item["event"],
                    "startTime": converted_item_start,
                    "endTime": converted_item_end,
                }
            )
    return converted_dict
