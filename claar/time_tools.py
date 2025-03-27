"""
Time constants and method
"""

import os
import uuid
from datetime import datetime, timedelta
import time
from typing import Optional, Callable

from claar import html

FORMAT_READABLE = '%d/%m/%y %H:%M:%S'
FORMAT_SORTABLE = '%Y%m%d_%H%M%S'


def today_str(format: str = "%Y%m%d") -> str:
    """
    Return today's date as a string formatted according to the specified format.

    This function retrieves the current date and formats it as a string using
    the provided date format pattern. If no format is specified, it defaults
    to the pattern "%Y%m%d".

    :param format: The format string used to represent the current date.
                        Defaults to "%Y%m%d".
    :return: A string representation of today's date in the specified format.
    """
    return datetime.today().strftime(format)


def now_str(format: str = "%Y_%m_%d_%H_%M_%S") -> str:
    """
    Converts the current date and time to a string using the specified format.

    The function takes a format string that defines how the current
    date and time should be represented as a string and returns
    the formatted string representation of the current date and time.
    The default format is "%Y_%m_%d_%H_%M_%S", which includes year,
    month, day, hour, minute, and second values separated by underscores.

    :param format: A string defining the desired format for the output date
        and time string. Defaults to "%Y_%m_%d_%H_%M_%S".
    :return: A string representation of the current date and time formatted
        according to the provided or default format.
    """
    return datetime.today().strftime(format)


def get_epoch() -> int:
    """
    Retrieve the current time expressed as the number of seconds since the epoch (January 1, 1970, 00:00:00 UTC).
    This function provides the timestamp in UNIX epoch format.

    :return: The current epoch time as an integer.
    """
    return int(time.time())


def seconds_since(timestamp: datetime) -> int:
    """
    Calculates the number of seconds that have passed since a given
    timestamp. If the given timestamp is None, the method will return
    0. This function computes the difference between the current time
    and the provided timestamp, returning the result in seconds.

    :param timestamp: A datetime object representing the starting point
        in time. If None, the function directly returns 0.
    :return: The number of seconds elapsed as an integer.
    """
    if timestamp is None:
        return 0
    time_difference = datetime.now() - timestamp
    return int(time_difference.total_seconds())


def generate_time_based_uid() -> str:
    """
    Generates a unique identifier (UID) based on the current time in microseconds. This function
    leverages time-based data combined with the `uuid5` algorithm to produce unique and deterministic
    identifiers. Useful for scenarios where time-sensitive unique IDs are required.

    :return: A unique identifier as a string.
    """
    current_time = int(time.time() * 1_000_000)  # Multiply to get microseconds
    uid = uuid.uuid5(uuid.NAMESPACE_DNS, str(current_time))
    return str(uid)


def safe_strptime(string: str, pattern: str) -> Optional[datetime]:
    """
    Try to convert string to time
    :param string: Value to convert
    :param pattern: Conversion pattern
    :return: struct_time value, or None in case of failure
    """
    try:
        return datetime.strptime(string, pattern)
    except ValueError as e:
        return None


def current_timezone() -> float:
    """
    Get the current timezone
    :return: timezone (float)
    """
    utc_offset_seconds = -time.timezone if time.localtime().tm_isdst == 0 else -time.altzone
    return utc_offset_seconds / 3600


def round_to_previous_quarter(timestamp: datetime) -> datetime:
    """
    Round a timestamp to the previous quarter of an hour
    :param timestamp: timestamp to round
    :return: timestamp rounded to the previous quarter
    """
    minutes_to_subtract = timestamp.minute % 15
    # Subtract the excess minutes and seconds, reset seconds, micro seconds
    rounded_dt = timestamp - timedelta(minutes=minutes_to_subtract,
                                       seconds=timestamp.second,
                                       microseconds=timestamp.microsecond)
    return rounded_dt


def labeled_sleep(delay: float,
                  text: str,
                  log_method: Optional[Callable[[str], None]]) -> None:
    """
    Log a message and sleep.
    :param delay: Time to sleep
    :param text: Message to log
    :param log_method: Logging method can be any method that takes 1 str argument
    """
    if log_method:
        log_method(text)
    else:
        print(text)
    time.sleep(delay)

class Lap:
    """
    Lap, like on a stopwatch
    """

    def __init__(self, base, previous, start, name="") -> None:
        self.base = base
        self.previous = previous
        self.start = start
        self.elapsed_since_start = start - base
        self.elapsed_since_previous = start - previous
        self.name = name

    def __repr__(self) -> str:
        return f"LAP '{self.name:30}' clicked at {self.start}, absolute {self.elapsed_since_start}, relative: {self.elapsed_since_previous}"

    def indented_repr(self, indent: int = 1) -> str:
        """
        Right alignment indent
        :param indent: number of characters
        """
        indent = max(indent, 1)  # Ensures minimum indent
        return f"LAP '{self.name:{indent}}' clicked at {self.start}, absolute {self.elapsed_since_start}, relative: {self.elapsed_since_previous}"


class Stopwatch:
    """
    A stopwatch class for measuring elapsed time and tracking laps.

    Provides functionality to track laps, reset the stopwatch, and represent the
    lap data in different formats such as a string or HTML representation.

    :ivar start: Timestamp marking when the stopwatch was started.
    :type start: datetime.datetime
    :ivar previous_click: Timestamp of the previous lap or click event.
    :type previous_click: datetime.datetime
    :ivar laps: List of recorded laps.
    :type laps: list[Lap]
    """

    def __init__(self) -> None:
        self.start = self.previous_click = datetime.now()
        self.laps = []

    def __repr__(self) -> str:
        indent = max([len(lap.name) for lap in self.laps])
        return os.linesep.join(self.lap_list(indent))

    # """ indent = 0 """ Generates issue '=' alignment not allowed in string format specifier
    def lap_list(self, indent=1) -> list:
        """
        Create list of lap descriptions
        """
        ret = [f"Timer started at: {self.start}"]
        for lap in self.laps:
            ret.append(f"{lap.indented_repr(indent)}")

        return ret

    def html(self) -> str:
        """
        Create an HTML representation of the stopwatch laps.
        """
        return f"""{html.BREAK.join(self.lap_list())}"""

    def click_start(self) -> None:
        """
        Reset the laps, set start time to now
        """
        self.start = self.previous_click = datetime.now()
        self.laps = []

    def click(self, lap_name="") -> None:
        """
        Registers a click event with an optional name,
        calculates the lap time, and updates the state.

        :param lap_name: The optional name associated with the click event.
        :return: None
        """
        new_click_time = datetime.now()
        lap = Lap(self.start, self.previous_click, new_click_time, lap_name)
        self.laps.append(lap)
        self.previous_click = new_click_time


if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
