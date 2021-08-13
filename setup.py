import os
import sys
from typing import Dict

import global_common

environment_variables: Dict[str, str] = {"KIH_API_TELEGRAM_BOT_TOKEN": "telegram bot token",
                                         "TELEGRAM_BOT_USERNAME": "Telegram bot username",
                                         "KIH_API_EMAIL_ACCOUNT": "outgoing email address",
                                         "KIH_API_EMAIL_ACCOUNT_PASSWORD": "email address' password",
                                         "KIH_API_DATABASE_HOST_NAME": "database' host's name",
                                         "KIH_API_DATABASE_HOST_IP": "database' host's IP",
                                         "KIH_API_DATABASE_USER_NAME": "database' host's username",
                                         "KIH_API_DATABASE_USER_NAME_PASSWORD": "database' host's password",
                                         "KIH_API_LOCATION_EXCEL_FILE": "financial database' excel file location",
                                         "TRANSFER_WISE_API_KEY": "TransferWise API Key"}


def set_environment_variable(key: str, value: str) -> None:
    if value == "":
        return
    elif sys.platform == "win32":
        global_common.run_command(["setx " + key + " \"" + value.replace("\"", "") + "\""])
    elif sys.platform == "linux":
        global_common.run_command([f"echo \"export {key}=\"{value}\" >> ~/.bash_profile"])
        global_common.run_command(["source ~/.bash_profile"])


if __name__ == "__main__":
    set_environment_variable("PYTHONPATH", os.getcwd())
    for key in environment_variables.keys():
        value: str = input("Enter the " + environment_variables[key] + ":")
        set_environment_variable(key, value)

print("\n\n----------------------------------------------------------------------------------")
print("Setup completed")
print("----------------------------------------------------------------------------------")
