"""
CSV related functions
"""

import csv
from typing import Optional, List


DEFAULT_DELIMITER = ";"


def load_csv(filename: str, delimiter=DEFAULT_DELIMITER) -> Optional[List[List[str]]]:
    """
    Load a CSV file into a two-dimensional list.
    :param filename: Location of the CSV file.
    :param delimiter: The delimiter used in the CSV file.
    :return: (data, message)
        - data: Two-dimensional list or None in case of error.
    """
    csv_data = []
    with open(filename) as file:
        reader = csv.reader(file, delimiter=delimiter)
        for row in reader:
            csv_data.append(row)
    return csv_data


def write_csv(filename: str,
              data: list,
              delimiter: str = DEFAULT_DELIMITER) -> bool:
    """
    Writes a list to a CSV file
    :param filename: Location of the CSV file.
    :param data: List to write.
    :param delimiter: The delimiter used in the CSV file.
    :return: Successful or not
    """
    with open(filename, mode='w') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(data)
    return True


if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
