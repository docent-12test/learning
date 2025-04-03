"""
OS directory related functions
"""

import base64
import hashlib
import os
import re
from datetime import datetime
from os import listdir
from os.path import isfile, join, getmtime
from typing import Optional, Union

from claar import tools

RENAME_LIMIT = 1000  # number limit when renaming file
NUMBER_OF_STALE_MOUNT_CHECKS = 3


def list_files(local_path: str,
               pattern: str = None,
               older_than: int = None,
               younger_than: int = None,
               full_path=True) -> Optional[list]:
    """
    List the files in a directory
    :param younger_than: list only files younger than this number of days
    :param older_than: list only files older  than this number of days
    :param local_path: path to look for files
    :param pattern: filename pattern to match
    :param full_path: if True the path is added to the filename(s)
    :return: list of  filenames
    """
    try:
        files = [f for f in listdir(local_path) if isfile(join(local_path, f))]
        if pattern is not None:
            files = [f for f in files if re.search(pattern, f)]
        if older_than is not None:
            files = [f for f in files if getmtime(join(local_path, f)) <= time.time() - 24 * 60 * 60 * older_than]
        if younger_than is not None:
            files = [f for f in files if getmtime(join(local_path, f)) >= time.time() - 24 * 60 * 60 * younger_than]
        if full_path:
            files = [join(local_path, f) for f in files]
        return files
    except RuntimeError as e:
        SCRIPT_LOGGER.debug(e)
        return None


def rename_with_date(file_name: str,
                     add_seconds: bool = False,
                     add_microseconds: bool = False) -> bool:
    """
    Add a timestamp extension to a filename,
    if that new filename already exists, an extra number extension is added
    :param add_microseconds: if true, add hh:mm:ss:microseconds to the extension
    :param add_seconds: if true, add hh:mm:ss to the extension
    :param file_name: Current file name
    :return: True if successful
    """
    extension_format = "%Y%m%d"
    if add_seconds or add_microseconds:
        extension_format += "%H%M%S"
        if add_microseconds:
            extension_format += "%f"
    name_with_date = f"{file_name}.{datetime.now().strftime(extension_format)}"
    if os.path.exists(name_with_date):
        i = 0
        temp_name = f"{name_with_date}.{i:4}"
        while os.path.isfile(temp_name):
            i += 1
            if i > RENAME_LIMIT:
                return False
            temp_name = f"{name_with_date}.{i:4}"
        os.rename(file_name, temp_name)
    else:
        os.rename(file_name, name_with_date)
    return True


def create_directory(path: str) -> bool:
    """
    Check if a directory create
    :param path: directory  to create
    :return: True if directory already exists or is created successfully
    """
    if os.path.isdir(path):
        SCRIPT_LOGGER.debug("Path {path} already exists as directory. "
                            "No need to recreate it")
        return True
    if os.path.exists(path):
        SCRIPT_LOGGER.debug("Path {path} already, but not as a directory."
                            " Can not create it")
        return False
    try:
        os.mkdir(path)
    except RuntimeError as e:
        SCRIPT_LOGGER.warning(f"Issue hen creating {path}. "
                              f"Can not create it ==> {e}")
        return False
    return True


def delete_list(file_list: list, base_dir: str = None) -> bool:
    """
    Delete a list of files
    :param file_list:  filenames to delete
    :param base_dir:base location for the file
    :return: True if all files have been deleted successfully
    """
    ok = True
    for file_name in file_list:
        if base_dir is None:
            full_name = file_name
        else:
            full_name = f"{base_dir}{os.path.sep}{file_name}"
        try:
            os.remove(full_name)
        except RuntimeError as e:
            SCRIPT_LOGGER.warning(f"Issue while deleting {full_name} ==> {e}")
            ok = False
    return ok


def file_contents(source_file: str, split: bool = False) -> Union[str, list]:
    """
    Get the contents of a file.
    :param source_file: file location
    :param split: if True the contents will be split in lines
    :return: String version of the file contents
    """
    f = open(source_file, "r")
    contents = f.read()
    f.close()
    if split:
        return contents.splitlines()
    return contents


def load_configfile(source_file: str) -> list:
    """
    Load the lines of a text file. Ignore empty lines or lines starting with #
    """
    ret = []
    lines = file_contents(source_file, True)
    for line in lines:
        line = line.strip()
        if len(line) == 0 or line.startswith("#"):
            continue
        ret.append(line)
    return ret


def file_prepend(target_file: str, text: str):
    """
    Add text at the beginning of a file
    Caution: do not use this with big files
    """
    with open(target_file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(text + content)


def file_contents_base64(source_file: str, encoding: str = "UTF-8") -> str:
    """
    Get the contents of a file.
    :param source_file: file location
    :param encoding: encoding
    :return: String version of the file contents
    """
    f = open(source_file, "rb")
    contents = f.read()
    f.close()
    return base64.b64encode(contents).decode(encoding)


DEFAULT_HASH_CHUNK = 4096
DEFAULT_HASH_ALGORITHM = "sha256"


def update_hash_with_chunks(file, hasher, chunk_size: int) -> None:
    """
    Update the hash object by reading the file in chunks.
    :param file: file object opened in binary mode
    :param hasher: hash object to be updated
    :param chunk_size: size of chunks to read from the file
    """
    while chunk := file.read(chunk_size):  # Using the walrus operator for simplicity
        hasher.update(chunk)


def file_hash(file_path: str,
              algorithm: str = DEFAULT_HASH_ALGORITHM,
              chunk_size: int = DEFAULT_HASH_CHUNK,
              log_error: bool = False) -> Optional[str]:
    """
    Generate a hash code for the contents of a file.

    :param file_path: Path to the target file
    :param algorithm: Hashing algorithm to use (default: sha256)
    :param chunk_size: Size (in bytes) of the file chunks to read (default: 4096)
    :param log_error: If True, logs the error in case of failure
    :return: Hash value of the file contents as a hexadecimal string, or None if an error occurred
    """
    hasher = hashlib.new(algorithm)
    with open(file_path, 'rb') as file:
        update_hash_with_chunks(file, hasher, chunk_size)
    return hasher.hexdigest()


def get_line_count(file_path: str) -> Optional[int]:
    """
    Counts the number of lines in the given file.

    :param file_path: Path to the input file
    :return: Number of lines in the file, or None if an error occurs
    """
    line_count = 0  # Initialize line count
    with open(file_path, 'rt') as file:
        for line_count, _ in enumerate(file, start=1):  # Start count at 1
            pass
    return line_count


def peek_line(infile, strip: bool = True) -> Optional[str]:
    """
    Reads the next line from a file object without advancing the read cursor.
    It provides a way to preview the line to be read next, with an option to
    strip whitespace from the line.

    :param infile: File object supporting `tell`, `readline`, and `seek` methods.
        This object should already be open and ready for reading.
    :param strip: Whether to strip leading and trailing whitespace from the
        previewed line. Defaults to True.
    :return: The next line in the file as a string, or None if the end of the
        file is reached.
    """
    original_position = infile.tell()
    line = infile.readline()
    infile.seek(original_position)
    should_strip_whitespace = line is not None and strip
    if should_strip_whitespace:
        line = line.strip()
    return line


if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
