import enum
import os
import subprocess
import threading
from decimal import Decimal
from typing import Any, Dict, Type, Optional, Callable, List, Union

import logger


def convert_string_to_dict(string: str) -> Dict[Any, Any]:
    parameters_list = string.split(",")

    return_dict = {}
    for parameter in parameters_list:
        key_value_pair = parameter.split("=")
        key = key_value_pair[0]
        value = key_value_pair[1]

        return_dict[key] = value

    return return_dict


def get_enum_from_value(value: Any, enum: Type[enum.Enum]) -> Optional[Any]:
    for enum_value in enum:
        if enum_value.value == value:
            return enum_value

    return None


def get_formatted_string_from_decimal(number: Decimal, decimal_places: int = 2) -> str:
    return f'{number.quantize(Decimal(10) ** -decimal_places):,}'


def run_as_separate_thread(target: Callable, arguments: tuple = ()) -> None:
    return_function: threading.Thread = threading.Thread(target=target, args=arguments)
    return_function.start()


def run_command(command_list: List[str]) -> Union[List[str], None]:
    output_list: List[str] = []

    for command in command_list:
        logger.info("Running command: " + command)
        output_list.extend(subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n"))

    for output in output_list:
        logger.info(output)

    return output_list


def get_running_processes(command: str) -> List[Dict[str, str]]:
    results_list: List[str] = run_command([f"sudo pgrep -a {command}"])

    processes_list: List[Dict[str, str]] = []
    for result in results_list:
        if command in result:
            processes_list.append({"PID": result.split(" ")[0], "Command": result.replace(result.split(" ")[0], "")})

    return processes_list


def kill_process(keyword: str, command: str) -> bool:
    processes_list: List[Dict[str, str]] = get_running_processes(command)
    is_process_found_and_killed = False

    for process in processes_list:
        if keyword in process["Command"]:
            run_command([f"kill -9 {process['PID']}"])
            is_process_found_and_killed = True

    return is_process_found_and_killed


def update_code_base(project_directory: str, main_branch_name: str = "main") -> None:
    os.chdir(project_directory)

    run_command([f"git reset --hard origin/{main_branch_name}"])
    run_command([f"git pull origin {main_branch_name}"])
