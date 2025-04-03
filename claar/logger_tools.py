"""
Logging capabilities of the framework
"""
import inspect
import logging
from dataclasses import dataclass
from typing import Union
from ansi import RED, BLUE, GREEN, YELLOW, WHITE, RESET, MAGENTA, BRIGHT_RED

SCRIPT_LOGGER_NAME = "SCRIPT"

SCRIPT_LOGGER = logging.getLogger(SCRIPT_LOGGER_NAME)
SCRIPT_LOGGER.setLevel(logging.DEBUG)


@dataclass
class LogLevelInfo:
    """
    Representation of logging level information.

    This class encapsulates information related to a specific logging level,
    including its name, associated label, display color, and the numerical
    level value. It can be used to define and organize log levels for
    logging systems.

    :ivar name: The name of the logging level.
    :type name: str
    :ivar label: The label associated with the logging level, typically used
        for display purposes.
    :type label: str
    :ivar color: The color associated with the logging level, represented
        as a string (e.g., a hex color code or color name).
    :type color: str
    :ivar level: The numerical value of the logging level, which typically
        determines its severity, where lower values indicate less severe
        levels and higher values more severe levels.
    :type level: int
    """
    name: str
    label: str
    color: str
    level: int


DebugInfo = LogLevelInfo(name="DEBUG", label="DEBUG", color=WHITE, level=logging.DEBUG)
InfoInfo = LogLevelInfo(name="INFO", label=" INFO", color=BLUE, level=logging.INFO)
WarningInfo = LogLevelInfo(name="WARNING", label=" WARN", color=GREEN, level=logging.WARNING)
ErrorInfo = LogLevelInfo(name="ERROR", label="ERROR", color=RED, level=logging.ERROR)
CriticalInfo = LogLevelInfo(name="CRITICAL", label=" CRIT", color=BRIGHT_RED, level=logging.CRITICAL)

LOG_LEVEL_NAMES = {CriticalInfo.name: logging.CRITICAL,
                   ErrorInfo.name: logging.ERROR,
                   WarningInfo.name: logging.WARNING,
                   InfoInfo.name: logging.INFO,
                   DebugInfo.name: logging.DEBUG}


def log_level_value(level: Union[int, str], default: int = logging.INFO) -> Union[int, str]:
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

    def __init__(self,
                 print_to_screen: bool = False) -> None:
        self.print_to_screen = print_to_screen

        self.logger = logging.getLogger(self.logger_name())
        logging.addLevelName(logging.DEBUG, DebugInfo.label)
        logging.addLevelName(logging.INFO, InfoInfo.label)
        logging.addLevelName(logging.WARNING, WarningInfo.label)
        logging.addLevelName(logging.ERROR, ErrorInfo.label)
        logging.addLevelName(logging.CRITICAL, CriticalInfo.label)

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
        for i in range(post_blanks):
            self._log_message(func)

    def debug(self,
              *messages,
              pre_blanks=0,
              post_blanks=0,
              color_code=DebugInfo.color):
        """
        Log a debug message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        :param color_code: ANSI Colour code
        """
        self._log_messages(self.logger.debug,
                           *messages,
                           pre_blanks=pre_blanks,
                           post_blanks=post_blanks,
                           color_code=color_code)

    def debug___(self,
                 *messages,
                 pre_blanks=0,
                 post_blanks=0,
                 color_code=DebugInfo.color):
        """
        Log a debug message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        :param color_code: ANSI Colour code
        """
        self.debug(*messages,
                   pre_blanks=pre_blanks,
                   post_blanks=post_blanks,
                   color_code=color_code)

    def info(self,
             *messages,
             pre_blanks=0,
             post_blanks=0,
             color_code=InfoInfo.color):
        """
        Log an info message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        :param color_code: ANSI Colour code
        """
        self._log_messages(self.logger.info,
                           *messages,
                           pre_blanks=pre_blanks,
                           post_blanks=post_blanks,
                           color_code=color_code)

    def info____(self,
                 *messages,
                 pre_blanks=0,
                 post_blanks=0,
                 color_code=InfoInfo.color):
        """
        Log an info message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        :param color_code: ANSI Colour code
        """
        self.info(*messages,
                  pre_blanks=pre_blanks,
                  post_blanks=post_blanks,
                  color_code=color_code)

    def warning(self,
                *messages,
                pre_blanks=0,
                post_blanks=0,
                color_code=WarningInfo.color):
        """
        Log a warning message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        :param color_code: ANSI Colour code
        """
        self._log_messages(self.logger.warning,
                           *messages,
                           pre_blanks=pre_blanks,
                           post_blanks=post_blanks,
                           color_code=color_code)

    def warning_(self,
                 messages,
                 pre_blanks=0,
                 post_blanks=0,
                 color_code=WarningInfo.color):
        """
        Log a warning message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        :param color_code: ANSI Colour code
        """
        self.warning(*messages,
                     pre_blanks=pre_blanks,
                     post_blanks=post_blanks,
                     color_code=color_code)

    def error(self,
              *messages,
              pre_blanks=0,
              post_blanks=0,
              color_code=ErrorInfo.color):
        """
        Log an error message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        :param color_code: ANSI Colour code
        """
        self._log_messages(self.logger.error,
                           *messages,
                           pre_blanks=pre_blanks,
                           post_blanks=post_blanks,
                           color_code=color_code)

    def error___(self,
                 *messages,
                 pre_blanks=0,
                 post_blanks=0,
                 color_code=ErrorInfo.color):
        """
        Log an error message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        :param color_code: ANSI Colour code
        """
        self.error(*messages,
                   pre_blanks=pre_blanks,
                   post_blanks=post_blanks,
                   color_code=color_code)

    def critical(self,
                 *messages,
                 pre_blanks=0,
                 post_blanks=0,
                 color_code=CriticalInfo.color):
        """
        Log a critical message.
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        :param messages: Message to log
        :param color_code: ANSI Colour code
        """
        self._log_messages(self.logger.critical,
                           *messages,
                           pre_blanks=pre_blanks,
                           post_blanks=post_blanks,
                           color_code=color_code)

    def log_trace(self,
                  level=logging.DEBUG,
                  top_level_only=True) -> None:
        """
        Logs the execution trace information.

        This method captures the call stack trace and logs its content up to the given
        level of detail. The primary purpose of this function is to provide insight
        into method calls and the execution path, which is useful for debugging and
        monitoring application behavior. The logging level can be customized, and the
        function allows restricting the information to just the top-level calling
        stack.

        :param level: The logging level at which the trace information will be logged.
        :param top_level_only: If True, logs only the top-level call in the stack trace. Defaults to True.

        :return: None
        """
        trace = inspect.stack()[1:]
        for row in trace:
            self.logger.log(level, row[3])
            if top_level_only:
                break



if __name__ == "__main__":
    # raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
    c = ClassLogger()
    c.logger.setLevel(logging.DEBUG)
    c.debug("This is a debug message")
    c.info("This is an info message")
    c.warning("This is a warning message")
    c.error("This is an error message")
    c.critical("This is a critical message")
