import time
from typing import Dict, Any

import database.constants
from logger import logger

start_time = time.time()
# database_connection = mysql.connector.connect(host=database.constants.database_host_name,
#                                               user=database.constants.database_user_name,
#                                               passwd=database.constants.database_user_name_password,
#                                               database=database.constants.database_name)
database_connection = None


# logger.debug(database.constants.execution_type__Database + "|" + "Connection Establishment" + "|" + start_time)


def insert(table_name: str, parameters: Dict[str, Any]) -> None:
    query = __get_insert_query(table_name, parameters)
    __execute_query(query)


def __get_insert_query(table_name: str, parameters_dict: Dict[str, Any]) -> str:
    column_names_query = ""
    values_query = ""

    i = 0
    while i < len(parameters_dict):
        column = list(parameters_dict.keys())[i]
        column_names_query = column_names_query + column

        value = parameters_dict[column]
        if isinstance(value, str):
            value = value.replace("\'", "\\'")
            if not value[:1] == "$":
                values_query = values_query + "'" + value + "'"
            else:
                values_query = values_query + value[1:]
        elif isinstance(value, int):
            values_query = values_query + str(value)
        else:
            raise Exception("Only string or ints are supported yet for value in key: " + column)

        if not i == (len(parameters_dict) - 1):
            column_names_query = column_names_query + ", "
            values_query = values_query + ", "

        i = i + 1

    query = "INSERT INTO `KIH-DB1`." + table_name + "(" + column_names_query + ") VALUES (" + values_query + ")"
    return query


def __get_select_query(table_name: str, parameters_dict: Dict[str, Any]) -> str:
    query = "SELECT * FROM `KIH-DB1`." + table_name + " WHERE "
    parameters_key = parameters_dict.keys()

    where_clause = ""
    loop_num = 1
    for parameter in parameters_key:
        if parameters_dict[parameter][:1] == "$":
            where_clause = where_clause + " " + parameter + " = " + parameters_dict[parameter]
        else:
            where_clause = where_clause + " " + parameter + " = '" + parameters_dict[parameter].replace("\\", "") + "'"

        if loop_num < len(parameters_dict):
            where_clause = where_clause + " AND "

    return query + where_clause


def __execute_query(query: str) -> None:
    # query.replace("©", "")
    # database_cursor = database_connection.cursor()
    #
    # # print("Executing query: " + query)
    #
    # start_time = time.time()
    # number_of_rows_affected = database_cursor.execute(query)
    # database_connection.commit()
    #
    # if query.lower().startswith("insert") and not query.lower().startswith("insert into `kih-db1`." + database.constants.table_Performance.lower()):
    #     logger.debug(database.constants.execution_type__Database + "|" + "INSERT" + "|" + query + "|" + start_time)
    # elif query.lower().startswith("update"):
    #     logger.debug(database.constants.execution_type__Database + "|" + "UPDATE" + "|" + query + "|" + start_time)
    #
    # return number_of_rows_affected
    pass


def select(query: str) -> Any:
    database_cursor = database_connection.cursor(buffered=True, dictionary=True)  # type: ignore

    # logger.debug("Executing query: " + query)

    start_time = time.time()
    database_cursor.execute(query)
    logger.debug(database.constants.execution_type__Database + "|" + "SELECT" + "|" + query + "|" + str(start_time))

    data = database_cursor.fetchall()
    return data
