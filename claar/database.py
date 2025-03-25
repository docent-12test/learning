"""
Database related functionality
"""

import os
import subprocess
from typing import Optional, Union, IO, List
import oracledb
from oracledb import Cursor

from lib import tools
from lib.constants import DatabaseTarget
from lib.data.matrix import Matrix

import server_config
from framework.exceptions import FrameworkException
from lib.logger_tools import SCRIPT_LOGGER
from lib.net import network

# String to be used as placeholder for method query_with_list
IN_LIST_CODE = "(((list)))"

# oracle specific limit of entries in a oracle clause: x in (.....)
MAX_ORACLE_LIST_SIZE = 999


def list_to_select_clause(list_to_convert: list,
                          enclosing_char: str = "") -> Optional[str]:
    """
     Convert a list to a comma-separated string, enclosed with specified characters.
    :param list_to_convert: Input list to be converted.
    :param enclosing_char: Character used to enclose each item.
    :return: Comma-separated string or None if input is invalid.
    """
    if not list_to_convert:
        SCRIPT_LOGGER.warning("List mag niet leeg zijn")
        return None
    if (isinstance(list_to_convert[0], str) and
            enclosing_char not in ['"', "'"]):
        SCRIPT_LOGGER.warning("list_to_select_clause - lijst  elementen "
                              "zijn van type string, maar er is geen "
                              "enclosing_char. Is het geen (dubbel)quote?")
    try:
        new_list = [f"{enclosing_char}{x}{enclosing_char}" for x in list_to_convert]
        return ", ".join(new_list)
    except Exception as e:
        raise FrameworkException(f"List to select failed => {e}")


def get_oracle_cursor(connection_group: dict = server_config.DB_INFO,
                      target: DatabaseTarget = DatabaseTarget.REP) -> Optional[Cursor]:
    """
    Get a connection to a specific server
    :param connection_group: connection group
    :param target: target within the group
    :return: Database cursor or None on failure
    """
    try:
        # Retrieve target servers
        servers = connection_group.get(target)
        if not servers:
            SCRIPT_LOGGER.error(f"Target {target} not found in connection group.")
            return None
        for server in servers:
            first = True
            for attempt in range(server_config.CONNECT_RETRIES):
                try:
                    if not first:
                        SCRIPT_LOGGER.debug(f"Database connect: {server} - "
                                            f"poging: {attempt + 1}/{server_config.CONNECT_RETRIES}")
                    first = False
                    connection = oracledb.connect(
                        dsn=server,
                        config_dir=server_config.ORACLE_CONFIG_DIR,
                        wallet_location=server_config.ORACLE_WALLET_LOCATION)
                    cursor = connection.cursor()
                    cursor.execute("ALTER SESSION SET TIME_ZONE='Europe/Paris'")
                    return cursor
                except oracledb.DatabaseError as e:
                    SCRIPT_LOGGER.error(f"Failed to connect to Oracle"
                                        f" on target {server} "
                                        f"(attempt: {attempt + 1}"
                                        f"=> {target}: {e}")
    except KeyError as e:
        SCRIPT_LOGGER.error(f"Target {target} not found in connection group: {e}")
    except Exception as e:
        SCRIPT_LOGGER.error(f"An unexpected error occurred: {e}")
    return None


def run_query(query: str,
              return_lists: bool = False,
              result_file: IO = None,
              target: DatabaseTarget = DatabaseTarget.REP,
              connection_group: dict = server_config.DB_INFO,
              **kwargs) -> Optional[list]:
    """
     Execute a database query and fetch results.

    :param query: SQL query to execute
    :param return_lists: If True, converts tuples in the result to lists
    :param result_file: File handle to write the query results; file must be open
                        (will be closed after writing).
    :param target: Target server group for execution
    :param connection_group: Database connection details
    :param query_params: Parameters for the SQL query
    :return: List of query results, where each row is a tuple (or a list if return_lists=True).
    """
    try:
        cursor = get_oracle_cursor(target=target,connection_group=connection_group)
        cursor.execute(query, kwargs)
        data = cursor.fetchall()
        if result_file is not None:
            for row in data:
                result_file.write(f"""{";".join(row)}{os.linesep}""")
            result_file.close()
        if return_lists:
            return [list(row) for row in data]
        return data
    except oracledb.Error as e:
        SCRIPT_LOGGER.critical(f"Query failed {query} with params {kwargs} => {e}")
    return None


def run_statement(query: str,
                  connection_group: dict = server_config.DB_INFO,
                  target: DatabaseTarget = DatabaseTarget.REP,
                  **kwargs) -> bool:
    """
    Run a statement.

    :param query: Query to execute
    :param connection_group: connection group
    :param target: connection target
    :param kwargs: value parameters of query
    :return: Successful or not
    """
    try:
        SCRIPT_LOGGER.debug(f"run_statement(): {query} {kwargs}")
        cursor = get_oracle_cursor(connection_group=connection_group, target=target)
        cursor.execute(query, kwargs)
        cursor.connection.commit()
        return True
    except oracledb.Error as e:
        SCRIPT_LOGGER.critical(f"Query failed {query} {kwargs} => {e}")
    return False


def get_query_matrix(query: str,
                     connection_group: dict = server_config.DB_INFO,
                     target: DatabaseTarget = DatabaseTarget.REP,
                     **kwargs) -> Optional[Matrix]:
    """
    Run a query.

    :param query: Query
    :param connection_group: connection_group
    :param target: target within the group
    :param kwargs: value parameters of query
    :return: Matrix
    """
    try:
        SCRIPT_LOGGER.debug(f"run_query(): {query} {kwargs}")
        cursor = get_oracle_cursor(connection_group=connection_group,
                                   target=target)
        cursor.execute(query, kwargs)
        headers = [item[0] for item in cursor.description]
        result_matrix = Matrix(headers=headers)
        data = cursor.fetchall()
        for row in data:
            result_matrix.add_row(row)
        return result_matrix
    except oracledb.Error as e:
        SCRIPT_LOGGER.critical(f"Query failed {query} {kwargs} => {e}")
        return None


# todo unittest
def run_count(query: str,
              connection_group: dict = server_config.DB_INFO,
              target: DatabaseTarget = DatabaseTarget.REP,
              **kwargs) -> Optional[int]:
    """
    Run a count query

    :param query: Query
    :param connection_group: connection_group
    :param target: target within the group
    :param kwargs: value parameters of query
    :return: Count result, None
    """
    q_res = run_query(query,
                      connection_group=connection_group,
                      target=target,
                      **kwargs)
    try:
        return q_res[0][0]
    except Exception as e:
        SCRIPT_LOGGER.debug(f"Error is running query {query} => {e}")
    return None


# todo: unittest for list set and tuple
def query_with_list(query: str,
                    input_list: Union[list, set, tuple],
                    return_lists: bool = False,
                    connection_group: dict = server_config.DB_INFO,
                    target: DatabaseTarget = DatabaseTarget.REP) -> Optional[list]:
    """
    Perform a query with an "in (list)" clause without exceeding
    Oracle's  max number of entries in the in clause.
    The query will be run several times, and the results will be appended.

    :param query: original query. The location (1 or more)
                  of the in-clause is marked with
    :param input_list: list to appear in the 'in (list)' clause
    :param return_lists: by default a list of tuples is returned.
                         If return_list is true then all tuples
                         will be converted to list
    :param connection_group: connection_group
    :param target: target within the group
    :return: result of the query
    """
    try:
        if not input_list:
            SCRIPT_LOGGER.debug("Can not query with empty list")
            return None
        enclosing_char = ""
        if isinstance(input_list, set):
            input_list = list(input_list)

        if isinstance(input_list[0], str):
            enclosing_char = "'"

        in_lists = tools.split_list(input_list, MAX_ORACLE_LIST_SIZE)
        ret = None
        for in_list in in_lists:
            q = query.replace(IN_LIST_CODE,
                              list_to_select_clause(in_list, enclosing_char))
            print(q)
            res = run_query(q,
                            return_lists=return_lists,
                            connection_group=connection_group,
                            target=target)
            ret = ret + res if ret is not None else res
        return ret
    except Exception as e:
        SCRIPT_LOGGER.debug(f"error {e} in {query}")
        return None


def get_query_result_single_row_single_column(query: str,
                                              connection_group: dict = server_config.DB_INFO,
                                              target: DatabaseTarget = DatabaseTarget.REP,
                                              **kwargs) -> Optional[str]:
    """
    Get a singleton (first row, first column) internals from a query result
    :param query: Query to execute
    :param connection_group: connection group
    :param target: target within the group
    :param kwargs: query parameters
    :return: Singleton internals
    """
    if len(kwargs) > 0:
        raise
    try:
        result = run_query(query, connection_group=connection_group, target=target)  # , kwargs)
        return result[0][0]
    except Exception:
        return None


def run_script_on_replication_server(script, server=None) -> (Optional[List], Optional[str]):
    """
    Run an oracle script on a server
    oracledb does not yet support complex PL/SQL scripts.
    Therefor: save the sql code to a file, run it with sqlplus and parse the output
    :param script: source of the script
    :param server: the database server to connect to
    :return: output rows  of the script in
    """
    if server:
        servers = [server]
    else:
        servers = network.get_rep_servers()
    SCRIPT_LOGGER.debug(f"Running script {script} on servers {servers}")
    if len(servers) == 0:
        return None, f"Could not run query because no servers found"
    error_message = ''
    for server in servers:
        try:
            sql = (f"whenever sqlerror exit 1 \n "
                   f"whenever oserror exit 2 \n @{script}")
            connection = f'/@{server}'
            session = subprocess.Popen(['sqlplus', '-S', connection],
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       text=True)
            session.stdin.write(sql)
            query_result, error_message = session.communicate()
            query_result = query_result.rstrip()
            if error_message == '' and session.returncode != 0:
                error_message = f"Error code {session.returncode}"
                raise Exception(error_message)
            if query_result != '' and query_result[0] == '\n':
                query_result = query_result[1:]
            return query_result, None
        except oracledb.Error as e:
            SCRIPT_LOGGER.critical(f"query failed on {server} ==> {e}")
    return None, f"Could not run query because it failed on all {len(servers)}: {error_message}"


# required for wallet connection
oracledb.init_oracle_client()

if __name__ == "__main__":
    raise NotImplementedError(__file__)
"""
FILE_INFORMATION=Fluvius;Arvid Claassen;Core of ANM framework
(C) Copyright 2024, Fluvius

Database related functionality
"""

import csv_tools
import os.path
import sqlite3 as db
from datetime import datetime
from itertools import chain
from sqlite3 import Connection, Error
from typing import Optional, Union

from lib import time_tools, tools
from lib.data.matrix import Matrix
from lib.logger_tools import SCRIPT_LOGGER

CONNECTION = None


def connect(filepath: str) -> None:
    """
    open a global connection to a database
    :param filepath: full path to db file
    """
    global CONNECTION
    CONNECTION = db.connect(filepath)




TABLE_NAME_WORKER_RESULTS = "worker_results"
TABLE_FRAMEWORK_AUDIT = "framework_audit"
TIME_FORMAT_SQLLITE = "%Y-%m-%d %H:%M:%f"
TIME_FORMAT_PYTHON = "%Y-%m-%d %H:%M:%S.%f"


def datetime_to_sqlite(timestamp: datetime = datetime.now()) -> str:
    """
    Convert a timestamp to the correct sqlite format
    :return: string format
    """
    return timestamp.strftime(TIME_FORMAT_PYTHON)[:-3]


def sqlite_to_timestamp(string: str) -> datetime:
    """
    Convert correct sqlite format to a timestamp
    Source: https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime
    :return: datetime
    """
    return datetime.strptime(string, TIME_FORMAT_PYTHON)


def create_worker_result_db(db_path: str) -> None:
    """
    Create a new result database for the current worker
    :param db_path: Location of the script
    """
    connection = db.connect(db_path)
    connection.execute(f"""
        CREATE TABLE {TABLE_NAME_WORKER_RESULTS} (
            result_worker INT NOT NULL,
            result_timestamp TEXT NOT NULL,
            result_code CHAR(255) NOT NULL,
            result_latest INT NOT NULL,
            result_type TEXT NOT NULL,
            result_value_text BLOB,           
            PRIMARY KEY (result_worker,result_timestamp,result_code)
        )        
                       """)
    connection.close()


def get_worker_db(db_path: str) -> db.Connection:
    """
    Get a connection to the result database
    :param db_path: path to databases
    :return: connection to the sqlite database
    """
    return db.connect(db_path)


def create_framework_audit_db(db_path: str) -> None:
    """
    Create a new result database for the current worker
    :param db_path: Location of the script
    """
    connection = db.connect(db_path)
    connection.execute(f"""
        CREATE TABLE if not exists {TABLE_FRAMEWORK_AUDIT}  (
            worker INT NOT NULL,
            uid TEXT,
            start_parameters TEXT,
            start_epoch int,             
            start_timestamp TEXT,
            end_epoch int,
            end_timestamp TEXT,
            delta,
            result TEXT,            
            PRIMARY KEY (uid)
        )""")
    connection.close()


def store_worker_audit_start(db_path: str, worker_id: int, uid: str, values: dict, start_epoch: int) -> (bool, str):
    """
    :param db_path: Full path to db file
    :param worker_id: id of the worker
    :param uid: some unique id
    :param values: start up parameters of the worker
    :param start_epoch: start epoch
    :return: successful, message
    """
    try:
        create_framework_audit_db(db_path)
        connection = db.connect(db_path)
        values = ";".join([f"{key}={value}" for key, value in values.items()]).replace("'", '')
        query = f"""insert into {TABLE_FRAMEWORK_AUDIT}(worker, uid, start_parameters, start_timestamp, start_epoch) values (
                        {worker_id}, '{uid}', '{values}', '{datetime_to_sqlite(datetime.now())}', {start_epoch} )"""
        connection.execute(query)
        connection.commit()
        connection.close()
        return True, None

    except Exception as e:
        return False, f"Probleem bij aanmaken van audit record {e}"


def store_worker_audit_stop(db_path: str, worker_id: int, uid: str, start_epoch: int) -> (bool, str):
    """
        :param db_path: Full path to db file
        :param worker_id: id of the worker
        :param uid: some unique id
        :param start_epoch: original start epoch (required to calculate run time)
        :return: successful, message
        """
    try:
        connection = db.connect(db_path)
        stop_epoch = time_tools.get_epoch_now()
        query = f"""update  {TABLE_FRAMEWORK_AUDIT} 
                    set end_timestamp = '{datetime_to_sqlite(datetime.now())}',
                        end_epoch = {stop_epoch}, 
                        delta = {stop_epoch - start_epoch}
                    where worker= {worker_id} and uid = '{uid}'"""
        connection.execute(query)
        connection.commit()
        connection.close()
        return True, None

    except Exception as e:
        return False, f"Probleem bij aanmaken van audit record {e}"


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


def execute_matrix(connection: db.Connection, query: str, *args) -> Optional[Matrix]:
    """
    Execute
    :param connection:
    :param query:
    :param args:
    :return:
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, args)
        headers = [item[0] for item in cursor.description]
        result_matrix = Matrix(headers=headers)
        data = cursor.fetchall()
        for row in data:
            result_matrix.add_row(row)
        return result_matrix
    except Exception as e:
        print(e)
        return None


def execute_statement(connection: Connection, statement: str, *args) -> Optional[int]:
    """
    Execute a SQL statement, e.g. DELETE, INSERT, UPDATE
    :param connection: sqlite3 connection
    :param statement: SQL statement
    :param args: optional arguments for the statement
    :return: Number of updated lines
    """
    try:
        cur = connection.cursor()
        cur.execute(statement, args)
        ret = cur.rowcount
        connection.commit()
        return ret
    except Exception as e:
        SCRIPT_LOGGER.critical(f"Error execution sqlite statement: {e}")
        return -1


def create_table(connection: Connection, name: str, definition: str, drop: bool = False, create_if_exists: bool = True) -> (bool, Optional[str]):
    """
    Create a table in the connected database
    :param connection: Connection to the sqlite3 db
    :param name: table name
    :param definition: tabel definitions
    :param drop: If True the existing table is dropped first
    :param create_if_exists: Recreate the table if it exists
    :return: Successful, Error msg
    """
    msg, ret = "", True
    try:
        cursor = connection.cursor()
        if drop:
            cursor.execute(f'DROP TABLE IF EXISTS {name}')
        infix = "IF NOT EXISTS " if create_if_exists else ""
        cursor.execute(f"CREATE TABLE {infix} {name} ({definition})")
        connection.commit()
    except Error as e:
        return False, f"{e}"
    return ret, msg


def get_query_result(connection: db.Connection, query: str, *args) -> Optional[Matrix]:
    """
    Run a query
    :param connection: connection to a database
    :param query: Query
    :param args: optional value parameters of query
    :return: Matrix result
    """
    try:
        cursor = connection.cursor()
        # SCRIPT_LOGGER.debug(f"run_query(): {query}")
        cursor.execute(query, args)
        headers = [item[0] for item in cursor.description]
        result_matrix = Matrix(headers=headers)
        data = cursor.fetchall()
        for row in data:
            result_matrix.add_row(row)
        return result_matrix
    except db.Error as e:
        print(f"Query failed {e}")
        return None


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


def get_all_tables(connection) -> Optional[list]:
    """
    Get all the tables in the database
    :param connection: open connection to the database
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        cursor.close()
        return chain.from_iterable(tables)  # turn  (('NAME1'),('NAME2')..., ('NAMEx')) to ['NAME1', 'NAME2', ... 'NAMEx']
    except Exception as e:
        SCRIPT_LOGGER.error(f"Error reading all tables from {connection} => {e}")
        return None


def dump_tables(connection: Union[Connection, str], target_dir: str, table_names=None) -> (bool, str):
    """
    Dump 1 or more tables file
    """
    try:
        # if a connection is supplied, then we leave it open.
        # If a connection string is supplied, then we close it afterward.
        must_close = False
        if isinstance(connection, str):
            connection = db.connect(connection)
            must_close = True
        if tools.none_or_empty(table_names):
            table_names = get_all_tables(connection)

        cursor = connection.cursor()
        for table_name in table_names or []:
            csv_file = os.path.join(target_dir, f"{table_name}.csv")

            # Fetch all rows from the table
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Write rows to CSV file
            with open(csv_file, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                # Write header
                csv_writer.writerow([i[0] for i in cursor.description])
                csv_writer.writerows(rows)  # Write data

            # Close the cursor and connection
        cursor.close()
        if must_close:
            connection.close()
    except Exception as e:
        return False, f"Error dumping table => {e}"


if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
