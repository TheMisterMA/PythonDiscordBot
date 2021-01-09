"""
File Name       :   data_handler.py
Project         :   ScheduleBot
Author          :   MrMA
Creation Date   :   17.12.20

This file defines the Bot's data handler, with it the bot could menege and stroe data more efficiently
"""

from json import dump, load
from json.decoder import JSONDecodeError
from discord import Message
from datetime import datetime


class BotDataHandler(object):
    """
    This class will handle certain information the bot needs to use even if it will go down.

    Parameters
    ----------
    file_path : str
        The file_path is used to specify where the Bot would store important data, such as schedualed meetings.
        Default value is 'Data.json'.

    Attributes
    ----------
    _data : Dictionary
        The data the bot is currently using for its actions.

    _file_path : str
        The file where the _data is uploded and uploads iin order to save data between sessions, where file_path is stored.
    """

    def __init__(self, file_path: str = "Data.json"):
        self._data = {}

        self._file_path = file_path

        #   If the json load function will raise an error the file is not in json format,
        #   then it will just dump into the file empty JSON.
        try:

            with open(self._file_path, "r") as json_file:
                self._data = load(json_file)
        except (FileNotFoundError, JSONDecodeError):

            with open(self._file_path, "w") as json_file:
                dump(self._data, json_file)

    def update_meetings(self, meeting_name: str, time: datetime):
        """
        Updates the meeting list, if the meeting does not exists it will create new meeting in the list.

        Parameters
        ----------
        meeting_name : str
            The souposed meeting's name.

        time : datetime
            The schedualed date and time the of the souposed meeting.
        """
        if self._data.get("Meetings") is None:
            self._data["Meetings"] = {}

        self._data["Meetings"][meeting_name] = {
            "Year":         time.year,
            "Month":        time.month,
            "Day":          time.day,
            "Hour":         time.hour,
            "Minute":       time.minute,
            "Second":       time.second,
            "Microsecond":  time.microsecond,
            "Reminders": 	{
                "WeekReminder": False,
                "DayReminder": 	False,
                "HourReminder":	False
            }
        }

        with open(self._file_path, "w") as json_file:
            dump(self._data, json_file)

    def get_meetings_scheduled_time(self, meeting_name: str) -> datetime or None:
        """
        Gets out of the data dictionary the date for the meeting, by its name.

        Parameters
        ----------
        meeting_name : str
            The meeting's name.

        Returns
        -------
        datetime or None
            Will return the date and the time of the meeting,
            if the meeting doesn't exist it will return a None.
        """
        if self._data.get("Meetings") is None or self._data["Meetings"].get(meeting_name) is None:
            return None

        return datetime(
            self._data["Meetings"][meeting_name]["Year"],
            self._data["Meetings"][meeting_name]["Month"],
            self._data["Meetings"][meeting_name]["Day"],
            self._data["Meetings"][meeting_name]["Hour"],
            self._data["Meetings"][meeting_name]["Minute"],
            self._data["Meetings"][meeting_name]["Second"],
            self._data["Meetings"][meeting_name]["Microsecond"])

    def get_meeting_names(self) -> list:
        """
        Gets all the meeting names set.

        Returns
        -------
        list
            A list of meeting names.
        """

        return [meeting_name for meeting_name in self._data["Meetings"]]

    def update_reminder(self, meeting_name: str, reminder: str) -> bool:
        """
        Updates the reminder fields, and returns if the field was actually updated.
        The boolean used to checkout wether the reminder was already used.

        Parameters
        ----------
        meeting_name : str
            The specified meeting's name.

        reminder : str
            The specific reminder to be updated or checked.

        Return
        ------
        bool
            True if the specified reminder field was updated.
            If the field wasn't updated, or the field is alredy done, it will return False.
        """

        #   Checks if the field\meeting\reminder exist, if not then it will return a false.
        #   If the field is already have been updated, then it will return a False.
        if self._data["Meetings"][meeting_name]["Reminders"].get(reminder) is None or self._data["Meetings"][meeting_name]["Reminders"].get(reminder):
            return False

        #   Else, it will update the reminder and dump the changes into the file.
        self._data["Meetings"][meeting_name]["Reminders"][reminder] = True

        with open(self._file_path, "w") as json_file:
            dump(self._data, json_file)

        #   Returns True for updating the file.
        return True

    def delete_meeting(self, meeting_name: str):
        """
        Deletes the meeting specified, and updates the file.

        Parameters
        ----------
        meeting_name : str
            The specified meeting's name.
        """
        if self._data["Meetings"].get(meeting_name) is not None:
            del self._data["Meetings"][meeting_name]

            with open(self._file_path, "w") as json_file:
                dump(self._data, json_file)
