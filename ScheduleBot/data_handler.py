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
            "Microsecond":  time.microsecond
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
