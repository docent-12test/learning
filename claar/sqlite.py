"""
Database related functionality
"""
import os
import sqlite3 as db
from datetime import datetime
from itertools import chain
from typing import Optional, Union, IO, Tuple
import csv

# String to be used as placeholder for method query_with_list
IN_LIST_CODE = "(((list)))"

# oracle specific limit of entries in a oracle clause: x in (.....)
MAX_LIST_SIZE = 999

CONN_TYPE = Union[str, db.Connection]
TIME_FORMAT_PYTHON = "%Y-%m-%d %H:%M:%S.%f"


def connect(full_path: str) -> (Optional[db.Connection], Optional[str]):
    """
    Establishes a connection to a database and returns the connection object along
    with any error message encountered during the process.

    The function attempts to connect to a database using the provided path. If an
    error is encountered during the connection process, it captures the error
    message and returns it along with a `None` value for the connection. If the
    connection is successful, it returns the connection object and `None` for
    the error message.

    :param full_path: The full filesystem path to the database file.
    :type full_path: str
    :return: A tuple containing the database connection object (or None if the
        connection failed) and the error message as a string (or None if no error
        occurred).
    :rtype: tuple[Optional[db.Connection], Optional[str]]
    """
    err = connection = None
    try:
        connection = db.connect(full_path)
    except db.Error as e:
        err = f"Error connecting to database: {e}"
    return connection, err


def get_cursor(connection: CONN_TYPE) -> (Optional[db.Cursor], Optional[str]):
    """
    Returns a database cursor and an optional error message based on the provided
    connection argument.

    This function takes a connection object or connection string and attempts to
    retrieve a cursor object from the database. If the connection string is
    provided, it attempts to establish a connection to the database before
    retrieving the cursor. If the connection or cursor creation fails, an
    error message is returned instead.

    :param connection: The database connection object or connection string.
    :type connection: Union[str, db.Connection]
    :return: A tuple containing the database cursor (or None if an error occurs)
        and an optional error message.
    :rtype: Tuple[Optional[db.Connection], Optional[str]]
    """
    err = cursor = None
    try:
        if isinstance(connection, str):
            connection = db.connect(connection)
        cursor = connection.cursor()
    except db.Error as e:
        err = f"Error connecting to database: {e}"
    return cursor, err


def run_query(query: str,
              conn: CONN_TYPE,
              return_lists: bool = False,
              result_file: IO = None,
              **kwargs) -> (Optional[list], Optional[str]):
    """
    Executes a database query, processes the result, and optionally writes it to
    a specified file or formats it as a list of lists. Returns the query result
    or a detailed error message if the query fails.

    :param query: The SQL query string to execute.
    :type query: str

    :param conn: The database connection object. This must provide a `cursor`
        method for creating a database cursor.
    :type conn: CONN_TYPE

    :param return_lists: Flag to indicate whether to convert the result rows into
        lists. Defaults to False.
    :type return_lists: bool, optional

    :param result_file: A writable file-like object to which the query results
        will be written. If None, output is not written to a file.
    :type result_file: IO, optional

    :param kwargs: Named parameters to substitute in the query. These will be
        passed to the query execution method.
    :type kwargs: dict

    :return: A tuple where the first element is either the query result as a list
        or None (depending on the success of the query and the `return_lists`
        parameter), and the second element is either None or an error message.
    :rtype: tuple[Optional[list], Optional[str]]
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, kwargs)
        data = cursor.fetchall()
        if result_file is not None:
            for row in data:
                result_file.write(f"""{";".join(row)}{os.linesep}""")
            result_file.close()
        if return_lists:
            return [list(row) for row in data]
        return data, None
    except db.Error as e:
        return None, f"Error running query {query} with params {kwargs} => {e}"


def run_statement(statement: str,
                  conn: CONN_TYPE,
                  **kwargs) -> (bool, Optional[str]):
    """
    Executes a given SQL statement using the provided connection and additional
    parameters, and commits the transaction. Returns the operation's success
    status and an error message if applicable.

    :param statement: SQL query to execute.
    :type statement: str
    :param conn: Database connection object to execute the query with.
    :type conn: CONN_TYPE
    :param kwargs: Additional parameters to substitute into the SQL query.
    :type kwargs: dict
    :return: A tuple where the first element is a boolean indicating whether the
        operation succeeded, and the second element is an optional error message.
    :rtype: tuple(bool, Optional[str])
    """
    try:
        cursor = get_cursor(conn)
        cursor.execute(statement, kwargs)
        cursor.connection.commit()
        return True, None
    except db.Error as e:
        return False, f"Query {statement} failed => {e} "


def run_count(query: str,
              conn: CONN_TYPE,
              **kwargs) -> (Optional[int], Optional[str]):
    """
    Executes a query to count entries in a database and handles potential errors. Returns the count
    as an integer or an error message if the query fails. The connection and query parameters must
    be provided, with additional parameters passed as keyword arguments.

    :param query: The SQL query string to execute.
    :type query: str
    :param conn: The database connection object.
    :type conn: CONN_TYPE
    :param kwargs: Additional keyword arguments to use with the query execution.
    :return: A tuple containing the count as an integer or None, and an error message as a string or None.
    :rtype: tuple[Optional[int], Optional[str]]
    """
    q_res = run_query(query, conn, **kwargs)
    try:
        return q_res[0][0], None
    except Exception as e:
        return None, f"Error running query {query} with params {kwargs} => {e}"


def query_with_list(query: str,
                    conn: CONN_TYPE,
                    input_list: Union[list, set, tuple],
                    return_lists: bool = False) -> (Optional[list], Optional[str]):
    """
    Execute a database query with an input list dynamically, handling various list types
    and configurations. This method splits large input lists into chunks and processes
    them iteratively to avoid exceeding query size limits. It supports dynamic query
    generation by replacing placeholders in the query string with the input list values.
    The method ensures string values are properly enclosed and handles empty input lists.

    :param query: The SQL query string, containing a placeholder for input list substitution.
    :type query: str
    :param conn: The database connection object to execute the query against.
    :type conn: CONN_TYPE
    :param input_list: The collection of values (list, set, or tuple) to iterate over in the query.
    :type input_list: Union[list, set, tuple]
    :param return_lists: Flag indicating whether to return results as lists or another format.
    :type return_lists: bool
    :return: A tuple containing the query results (if any) and an error message in case of failure.
    :rtype: Tuple[Optional[list], Optional[str]]
    """
    try:
        if not input_list:
            return None, "Can not query with empty list"
        enclosing_char = ""
        if isinstance(input_list, set):
            input_list = list(input_list)

        if isinstance(input_list[0], str):
            enclosing_char = "'"

        in_lists = tools.split_list(input_list, MAX_LIST_SIZE)
        ret = None
        for in_list in in_lists:
            q = query.replace(IN_LIST_CODE,
                              list_to_select_clause(in_list, enclosing_char))
            print(q)
            res = run_query(q,
                            conn,
                            return_lists=return_lists)
            ret = ret + res if ret is not None else res
        return ret
    except Exception as e:
        return None, f"error {e} in {query}"


def datetime_to_sqlite(timestamp: datetime) -> str:
    """
    Convert a timestamp to the correct sqlite format
    :return: string format
    """
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime(TIME_FORMAT_PYTHON)[:-3]


def sqlite_to_timestamp(string: str) -> datetime:
    """
    Convert correct sqlite format to a timestamp
    Source: https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime
    :return: datetime
    """
    return datetime.strptime(string, TIME_FORMAT_PYTHON)


def execute(connection: db.Connection, query: str, *args) -> Optional[list]:
    """
    Execute
    :param connection:
    :param query:
    :param args:
    :return:
    """
    try:
        cur = connection.cursor()
        cur.execute(query, args)
        connection.commit()
        return cur.fetchall()
    except Exception as e:
        print(e)
        return None


def create_table(connection: CONN_TYPE, name: str,
                 definition: str,
                 drop: bool = False,
                 create_if_exists: bool = True) -> (bool, Optional[str]):
    """
    Creates a database table with the specified name and definition. Depending on the
    parameters, it can drop the table if it exists and re-create it, or skip table creation
    if the table already exists.

    This function interacts with a database connection to execute the required SQL
    statements and handle table creation logic. Upon encountering any errors during SQL
    execution or connection handling, it returns appropriate details.

    :param connection: Database connection object used to interact with the database.
    :type connection: CONN_TYPE
    :param name: The name of the table to be created in the database.
    :type name: str
    :param definition: SQL definition for the table schema, defining its columns
        and their data types.
    :type definition: str
    :param drop: Flag indicating whether to drop the existing table before
        creating a new one. Default is False.
    :type drop: bool
    :param create_if_exists: Flag specifying whether to conditionally create the
        table only if it does not already exist. Default is True.
    :type create_if_exists: bool
    :return: A tuple where the first element is a boolean indicating success
        (True) or failure (False), and the second element is an optional string
        containing an error message if any issues occurred, otherwise an empty
        string.
    :rtype: (bool, Optional[str])
    """
    msg, ret = "", True
    try:
        cursor = connection.cursor()
        if drop:
            cursor.execute(f'DROP TABLE IF EXISTS {name}')
        infix = "IF NOT EXISTS " if create_if_exists else ""
        cursor.execute(f"CREATE TABLE {infix} {name} ({definition})")
        connection.commit()
    except db.Error as e:
        return False, f"{e}"
    return ret, msg


def get_or_create_database(filename: str, create_statement: str) -> db.Connection:
    """
    Open a database file. If it does not exist, create it
    :param filename: full file path of the database
    :param create_statement: SQL create statement in case the database does not exit
    :return: connection to the database
    """
    if os.path.exists(filename):
        return db.connect(filename)
    connection = db.connect(filename)
    connection.execute(f"""{create_statement}"""")")
    return connection


def get_all_tables(connection) -> (Optional[list], Optional[str]):
    """
    Fetches the names of all tables from a SQLite database connection.

    This function attempts to retrieve all table names from the database connected
    through the provided connection object. It uses an SQL command to query the
    SQLite master table for all tables. If successful, it returns a list of table
    names. In the event of any error, it returns None and an error message.

    :param connection: Database connection object to the SQLite database.
    :return: A tuple where the first element is a list of table names or None, and
             the second element is an error message in case of failure, otherwise None.
    """
    try:
        cursor = get_cursor(connection)
        cursor.execute("""SELECT name 
                            FROM sqlite_master 
                           WHERE type='table'""")
        tables = cursor.fetchall()
        cursor.close()
        # turn  (('NAME1'),('NAME2')..., ('NAMEx')) to ['NAME1', 'NAME2', ... 'NAMEx']
        return chain.from_iterable(tables), None
    except Exception as e:
        return None, f"Error reading all tables from {connection} => {e}"


def export_tables_to_csv(connection: CONN_TYPE,
                         target_directory: str,
                         table_names: Optional[list] = None) -> (bool, Optional[str]):
    """
    Exporteert gegevenstabellen naar afzonderlijke CSV-bestanden in een opgegeven doelmap.

    :param connection: Een verbinding of een verbindingsreeks met de database.
    :param target_directory: De map waarin de CSV-bestanden opgeslagen moeten worden.
    :param table_names: Een lijst van tabellen die geëxporteerd moeten worden (optioneel).
    :return: (bool, str) of het is geslaagd en een foutbericht indien van toepassing.
    """
    try:
        # Bepalen of we verbinding handmatig moeten sluiten
        must_close_connection = False
        if isinstance(connection, str):
            connection = db.connect(connection)
            must_close_connection = True

        if not table_names:
            table_names = get_all_tables(connection)

        cursor = connection.cursor()

        for table_name in table_names:
            # Voor elke tabel, schrijf naar een apart CSV-bestand
            try:
                res, err = write_table_to_csv(cursor, table_name, target_directory)
                if not res or err:
                    return False, f"Fout bij schrijven van tabel {table_name} naar CSV: {err}"
            except Exception as e:
                return False, f"Fout bij schrijven van tabel {table_name} naar CSV: {e}"
        cursor.close()

        # Sluiten van de databaseverbinding indien nodig
        if must_close_connection:
            connection.close()

        return True, None
    except Exception as e:
        return False, f"Algemene fout bij het exporteren van tabellen: {e}"


def write_table_to_csv(cursor,
                       table_name: str,
                       output_directory: str) -> (bool, Optional[str]):
    """
    Writes the content of a database table to a CSV file.

    This function reads the specified `table_name` from the database using
    the `cursor` provided and writes its content to a CSV file in the specified
    `output_directory`. The CSV file will be named after the table with a `.csv`
    extension. If an exception occurs during the process, the function returns
    a failure status with the corresponding error message.

    :param cursor: A database cursor for executing SQL queries and fetching results.
    :param table_name: The name of the database table to be exported to the CSV file.
    :param output_directory: The directory where the resulting CSV file will be saved.
    :return: A tuple consisting of a boolean indicating the success status and an optional
             string with an error message in case of failure.
    :rtype: Tuple[bool, Optional[str]]
    """
    try:
        csv_file_path = os.path.join(output_directory, f"{table_name}.csv")
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Schrijf kolomkoppen en rijen
            csv_writer.writerow([column[0] for column in cursor.description])  # Kolomkop
            csv_writer.writerows(rows)  # Data-rijen
            return True, None
    except Exception as e:
        return False, f"Fout bij schrijven van tabel {table_name} naar CSV: {e}"


if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
