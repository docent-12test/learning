"""
FILE_INFORMATION=Fluvius;Arvid Claassen;Core of ANM framework
(C) Copyright 2024, Fluvius

Logging capabilities of the framework
"""
import inspect
import logging
from typing import Union

import server_config
from lib.formatting import YELLOW, RED, GREEN, GRAY, RESET, BLUE

SCRIPT_LOGGER_NAME = "SCRIPT"
FRAMEWORK_LOGGER_NAME = "FRAMEWORK"

SCRIPT_LOGGER = logging.getLogger(SCRIPT_LOGGER_NAME)
SCRIPT_LOGGER.setLevel(logging.DEBUG)

FRAMEWORK_LOGGER = logging.getLogger(FRAMEWORK_LOGGER_NAME)
FRAMEWORK_LOGGER.setLevel(logging.INFO)

CRITICAL = 'CRITICAL'  # Deze waarde niet aanpassen, want ze moet overeenkomen met de level-naam in DMS
ERROR = 'ERROR'  # Deze waarde niet aanpassen, want ze moet overeenkomen met de level-naam in DMS
WARNING = 'WARNING'  # Deze waarde niet aanpassen, want ze moet overeenkomen met de level-naam in DMS
INFO = 'INFO'  # Deze waarde niet aanpassen, want ze moet overeenkomen met de level-naam in DMS
DEBUG = 'DEBUG'  # Deze waarde niet aanpassen, want ze moet overeenkomen met de level-naam in DMS

# Deze waardes niet aanpassen, want ze moet overeenkomen met de level-naam in DMS
LOG_LEVEL_NAMES = {CRITICAL: logging.CRITICAL,
                   ERROR: logging.ERROR,
                   WARNING: logging.WARNING,
                   INFO: logging.INFO,
                   DEBUG: logging.DEBUG}

LOGFILE_LABEL_CRITICAL = ' CRIT'  # Deze waarde mag aangepast worden, heeft enkel invloed op label in log file
LOGFILE_LABEL_ERROR = 'ERROR'  # Deze waarde mag aangepast worden, heeft enkel invloed op label in log file
LOGFILE_LABEL_WARNING = ' WARN'  # Deze waarde mag aangepast worden, heeft enkel invloed op label in log file
LOGFILE_LABEL_INFO = ' INFO'  # Deze waarde mag aangepast worden, heeft enkel invloed op label in log file
LOGFILE_LABEL_DEBUG = 'DEBUG'  # Deze waarde mag aangepast worden, heeft enkel invloed op label in log file


# Unittest OK
def log_level_value(level: Union[int, str], default: int = server_config.LOG_DEFAULT_LEVEL) -> Union[int, str]:
    """
    Get the numeric log level
    :param level:
        If level is numeric, then check whether the value corresponds to a known log level.
        If level is string, then check if the level corresponds to a known log level name.
    :param default: default
    Numeric value of the test level or the default version
    """
    if isinstance(level, int) and level in LOG_LEVEL_NAMES.values():
        return level
    elif isinstance(level, str) and level in LOG_LEVEL_NAMES.keys():
        return LOG_LEVEL_NAMES[level]
    return default


def parse_log_level_name(level_name: str) -> int:
    """
    Translate log level name to log level value
    :param level_name: log level name to parse
    :return: correct log level value or debug in case of parsing errors
    """
    return LOG_LEVEL_NAMES.get(level_name, logging.DEBUG)


class ClassLogger:
    """
    Class to extend takes an external log and adds log functions
    """

    def __init__(self, **kwargs) -> None:
        self.print_to_screen = False
        value = kwargs.get('print')

        if value is not None and value:
            self.print_to_screen = True
        else:
            self.print_to_screen = server_config.FRAMEWORK_STDOUT_LOGGING
        self.logger = logging.getLogger(self.logger_name())
        logging.addLevelName(logging.DEBUG, LOGFILE_LABEL_DEBUG)
        logging.addLevelName(logging.INFO, LOGFILE_LABEL_INFO)
        logging.addLevelName(logging.WARNING, LOGFILE_LABEL_WARNING)
        logging.addLevelName(logging.ERROR, LOGFILE_LABEL_ERROR)
        logging.addLevelName(logging.CRITICAL, LOGFILE_LABEL_CRITICAL)

    def __repr__(self):
        return f"{self.__class__.__name__} with logger: {self.logger_name()}"

    def logger_name(self):
        """
        By default, the logger for this class is identified by its class name.
        This method should be overloaded if instances want to share a loggers by returning a globally known name.
        :return: Class name
        """
        return self.__class__.__name__

    def _log_message(self, func, message="") -> None:
        """
        Log a message using the provided function.
        If the print_to_screen option is activated, the message will be printed as well
        :param func: logging function
        :param message: message to print
        """
        if self.print_to_screen:
            print(message)
        func(message)

    def _log_messages(self,
                      func,
                      *messages,
                      pre_blanks=0,
                      post_blanks=0,
                      color_code="") -> None:
        """
        Log a message using the provided function.
        If the print_to_screen option is activated, the message will be printed as well
        :param func: logging function
        :param message: message to print
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        :param color_code: ANSI Colour code
        """

        for i in range(pre_blanks):
            self._log_message(func)
        for message in messages:
            self._log_message(func, f"{color_code}{message}{RESET}")
            # func(message)
        for i in range(post_blanks):
            self._log_message(func)

    def debug(self, *messages, pre_blanks=0, post_blanks=0):
        """
        Log a debug message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        self._log_messages(self.logger.debug,
                           *messages,
                           pre_blanks=pre_blanks,
                           post_blanks=post_blanks,
                           color_code=GRAY)

    def debug___(self, *messages, pre_blanks=0, post_blanks=0):
        """
        Log a debug message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        self.debug(*messages, pre_blanks=pre_blanks, post_blanks=post_blanks)

    def info(self, *messages, pre_blanks=0, post_blanks=0):
        """
        Log an info message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        self._log_messages(self.logger.info,
                           *messages,
                           pre_blanks=pre_blanks,
                           post_blanks=post_blanks,
                           color_code=BLUE)

    def info____(self, *messages, pre_blanks=0, post_blanks=0):
        """
        Log an info message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        self.info(*messages, pre_blanks=pre_blanks, post_blanks=post_blanks)

    def warning(self, *messages, pre_blanks=0, post_blanks=0):
        """
        Log a warning message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        self._log_messages(self.logger.warning,
                           *messages,
                           pre_blanks=pre_blanks,
                           post_blanks=post_blanks,
                           color_code=GREEN)

    def warning_(self, messages, pre_blanks=0, post_blanks=0):
        """
        Log a warning message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        self.warning(*messages, pre_blanks=pre_blanks, post_blanks=post_blanks)

    def error(self, *messages, pre_blanks=0, post_blanks=0):
        """
        Log an error message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        self._log_messages(self.logger.error,
                           *messages,
                           pre_blanks=pre_blanks,
                           post_blanks=post_blanks,
                           color_code=RED)

    def error___(self, *messages, pre_blanks=0, post_blanks=0):
        """
        Log an error message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        self.error(*messages,
                   pre_blanks=pre_blanks,
                   post_blanks=post_blanks)

    def critical(self, *messages, pre_blanks=0, post_blanks=0):
        """
        Log a critical message.
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        :param messages: Message to log
        """
        self._log_messages(self.logger.critical,
                           *messages,
                           pre_blanks=pre_blanks,
                           post_blanks=post_blanks,
                           color_code=YELLOW)

    def log_trace(self, level=logging.DEBUG, top_level_only=True):
        """
        Log the name of the calling method
        """
        trace = inspect.stack()[1:]
        for row in trace:
            self.logger.log(level, row[3])
            if top_level_only:
                break


class ScriptLogger(ClassLogger):
    """
    Default script logger
    """

    def logger_name(self) -> str:
        """
        Return the global name of the script logger
        :return:
        """
        return SCRIPT_LOGGER_NAME


class FrameworkLogger(ClassLogger):
    """
    default script logger
    """

    def logger_name(self) -> str:
        """
        Return the global name of the script logger
        :return:
        """
        return FRAMEWORK_LOGGER_NAME



if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
