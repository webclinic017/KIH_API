import logging
import time
from typing import Any, Dict

import database.constants

logger = logging.getLogger();

logger.setLevel(logging.DEBUG)


# logger.setLevel(logging.INFO)
# logger.setLevel(logging.WARNING)
# logger.setLevel(logging.ERROR)
# logger.setLevel(logging.CRITICAL)

def debug(message: str) -> None:
    print("DEBUG | " + str(message))
    logger.debug(str(message))
    __insert_into_log_table(message, "DEBUG")


def info(message: str) -> None:
    print("INFO | " + str(message))
    logger.info(str(message))
    __insert_into_log_table(message, "INFO")


def error(message: str) -> None:
    print("ERROR | " + str(message))
    logger.error(str(message))
    __insert_into_log_table(message, "ERROR")


def performance(execution_type: str, execution_subtype: str, execution_command: str, start_time: float, description: str = None) -> None:
    time_taken: int = int((time.time() - start_time) * 1000)

    parameters: Dict[str, Any] = {database.constants.column_Performance__Application:
                                      database.constants.database_application_name,
                                  database.constants.column_Performance__Execution_Type: execution_type,
                                  database.constants.column_Performance__Execution_Subtype: execution_subtype,
                                  database.constants.column_Performance__Execution_Command: execution_command,
                                  database.constants.column_Performance__Execution_Time: time_taken}
    database.insert(database.constants.table_Performance, parameters)

    log_message: str = str(time_taken) + "ms || Execution Type: " + execution_type + " | Execution Subtype:  " + execution_subtype
    if description is not None:
        log_message = log_message + " | " + description

    print(log_message)


def __insert_into_log_table(message: str, logger_level: str) -> None:
    parameters = {database.constants.column_Log__Application: database.constants.database_application_name,
                  database.constants.column_Log__Logger_Level: logger_level,
                  database.constants.column_Log__Log: message}
    database.insert(database.constants.table_Log, parameters)
