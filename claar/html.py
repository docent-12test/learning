"""
HTML related functionality
"""
from typing import Union, Optional

TABLE_OPEN = "<TABLE border=1>"
TABLE_CLOSE = "</TABLE>"
ROW_OPEN = "<TR>"
ROW_CLOSE = "</TR>"
TABLE_HEADER_OPEN = "<TH>"
TABLE_HEADER_CLOSE = "</TH>"
TABLE_CELL_OPEN = "<TD>"
TABLE_CELL_CLOSE = "</TD>"
BREAK = "<BR/>"
HORIZONTAL_LINE = "<HR/>"

STRONG_OPEN = "<STRONG>"
STRONG_CLOSE = "</STRONG>"

EMPTY_CELL = f"{TABLE_CELL_OPEN}no data{TABLE_CELL_CLOSE}"


# unittest OK
def enclose(msg: str, tag: str, style: str = "") -> str:
    """
    Enclose a message between HTML tags,
    :param msg: Message to enclose
    :param tag: Tag to enclose with
    :param style: style attributes to add to the opening tag.
    :return: Enclosed message <tag style>message</tag>
    """
    if style is not None and style != "":
        return f"<{tag} style='{style}'>{msg}</{tag}>"
    else:
        return f"<{tag}>{msg}</{tag}>"


# unittest OK
def strong(msg: str, style: str = "") -> str:
    """
    Turn the message to an BOLD html text
    :param msg: message
    :param style: optional style
    :return:  message enclosed.
    """
    return enclose(msg, "STRONG", style)


# unittest OK
def italic(msg: str, style: str = "") -> str:
    """
    Turn the message to an BOLD html text
    :param msg: message
    :param style: optional style
    :return:  message enclosed.
    """
    return enclose(msg, "I", style)


# unittest OK
def underline(msg: str, style: str = "") -> str:
    """
    Turn the message to an BOLD html text
    :param msg: message
    :param style: optional style
    :return:  message enclosed.
    """
    return enclose(msg, "U", style)


def href(link: str, description: str) -> str:
    """
    Compose a href
    :param link: url
    :param description: text to display
    :return: html code
    """
    return f"<A HREF='{link}'>{description}</A>"


def list_to_table_row(row: Optional[list], include_row_tag: bool = True) -> str:
    """
    Convert a list into a row in an HTML table
    :param row: list to convert
    :param include_row_tag: if true thr result will be enclosed in a TR tag
     :return: html code
    """
    html_code = ""
    if row is not None:
        for value in row:
            html_code += f"{TABLE_CELL_OPEN}{value}{TABLE_CELL_CLOSE}"
    if include_row_tag:
        return f"{ROW_OPEN}{html_code}{ROW_CLOSE}"
    return html_code


def html_table(input_list: list):
    """
    Create an HTML table from a list[list]
    :param input_list: list to represent in HTML
    :return: HTML code
    """
    html_code = TABLE_OPEN
    for row in input_list or []:
        html_code += ROW_OPEN
        for element in row or []:
            html_code += f"{TABLE_CELL_OPEN}{element}{TABLE_CELL_CLOSE}"
        html_code += ROW_CLOSE
    html_code += TABLE_CLOSE
    return html_code


# todo: unittest
def replace_html_entities(source: str, character_list: Union[tuple, list, set] = ('&', '<', '>', '/', '%', '\\', '\'', '\"')) -> str:
    """
    Replace unsafe characters with their entity representation.
    :param source: Input string
    :param character_list: list of unsafe which characters to consider unsafe. The default is ('&', '<', '>',  '\'', '\"')
    :return: string with safe character
    """
    ret = source
    for char in character_list:
        ret = ret.replace(char, f"&#{ord(char)};")
    return ret



if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
