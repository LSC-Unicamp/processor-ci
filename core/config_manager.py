import os
import sys
import json
from time import time


CONFIG_FILE = "config.json"


def open_config_file() -> dict[str, any]:
    print(f"Log: Opening {CONFIG_FILE} file")

    if not os.path.isfile(CONFIG_FILE):
        sys.exit(f"[ {time()} ] Error: {CONFIG_FILE} file not found.")

    file = open(CONFIG_FILE, "r")

    data: dict[str, any] = json.load(file)

    file.close()

    print(f"Log: {CONFIG_FILE} file opened successfully.")

    return data
