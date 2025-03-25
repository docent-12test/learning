"""
FILE_INFORMATION=Fluvius;Arvid Claassen;Core of ANM framework
(C) Copyright 2024, Fluvius

OS
"""

from os import getloadavg
from time_tools import sleep

from lib import time_tools
from lib.logger_tools import SCRIPT_LOGGER

LOAD_LOOP_DELAY = 1  # number of seconds to sleep during loop to sync
LOAD_LOOP_MAX = 1000  # max number of loops to wait until syc wait breaks
LOAD_DEFAULT_THRESHOLD = 4  # load avg


def get_avg_load_01():
    """
    Get avg load for last minute
    """
    return getloadavg()[0]


def get_avg_load_1():
    """
    Get avg load for last minute
    """
    return get_avg_load_01()


def get_avg_load_05():
    """
    Get avg load for last 5 minutes
    """
    return getloadavg()[1]


def get_avg_load_5():
    """
    Get avg load for last 5 minutes
    """
    return get_avg_load_05()


def get_avg_load_15():
    """
    Get avg load for last 15 minutes
    """
    return getloadavg()[2]


def wait_for_load(threshold: float = LOAD_DEFAULT_THRESHOLD,
                  delay: float = LOAD_LOOP_DELAY,
                  max_iterations: int = LOAD_LOOP_MAX):
    """
    Wait until current server load is below threshold
    :param threshold: max allowed load
    :param delay: number of seconds to sleep between checks
    :param max_iterations: max number of iterations (stop condition of the loop)
    :return: number of seconds it took until server is below load
    """
    SCRIPT_LOGGER.debug(f"Checking if server load is below {threshold}.")
    i = 0
    start_epoch = time_tools.get_epoch_now()
    while i < max_iterations and get_avg_load_1() >= threshold:
        i += 1
        SCRIPT_LOGGER.warning(f"Load is too high, sleeping {delay} seconds")
        sleep(delay)
    return time_tools.get_epoch_now() - start_epoch


if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
