import os
import time
from datetime import date
import json

with open(os.path.join("data", "metadata.json"), "r") as f:
    metadata = json.load(f)

NAME = metadata.get("name", "Failed to fetch name")
DESCRIPTION = metadata.get("description", "Failed to fetch description")
COPYRIGHT = metadata.get("copyright", "Failed to fetch copyright")
LICENSE = metadata.get("license", "Failed to fetch license")
VERSION = metadata.get("version", "Failed to fetch version")
BUILDVER = metadata.get("buildver", "Failed to fetch build version")
REPO = metadata.get("repo", "Failed to fetch repository URL")

AHK_PATH = os.path.abspath(os.path.join("AutoHotKey", "ahk.exe"))


def logmessage(status, message, member: str = None, function: str = None):
    """A dynamic helper function for printing advanced log messages.
    Args:
        status (str): The status of the log message (e.g., 'info', 'error').
        message (str): The message to log.

        member (str, optional): The member associated with the log message.
        function (str, optional): The function associated with the log message.
    """

    current_time = time.strftime("%H:%M:%S", time.localtime())
    today = date.today()

    gray = "\033[90m"       # gray for timestamp
    status_colors = {
        "debug": "\033[94m",      # blue
        "info": "\033[92m",       # green
        "warning": "\033[93m",    # yellow
        "error": "\033[91m",      # red
        "notice": "\033[95m",     # magenta
    }
    function_color = "\033[96m"   # cyan
    member_color = "\033[38;5;136m" # dark yellow
    reset_color = "\033[0m" # end of color

    status_text = status.upper()
    status_color = status_colors.get(status.lower(), reset_color)

    log_entry = (
        f"{gray}{today} {current_time}{reset_color} " # Date, Time
        f"[{status_color}{status_text}{reset_color}]" # Status
    )

    # If specified, append args to the log entry
    if member:
        log_entry += f" [{member_color}{member.upper()}{reset_color}]"
    if function:
        log_entry += f" [{function_color}{function.upper()}{reset_color}]"

    log_entry += f" {message}"


    try:
        entry = f"{today} {current_time} [{status_text}]"

        if member:
            entry += f" [{member.upper()}]"
        if function:
            entry += f" [{function.upper()}]"

        entry += f" {message}\n"

        with open(os.path.join("data", "log.log"), "a", encoding="utf-8") as f:
            f.write(entry)

    except Exception as e:
        print(f"Failed to write to log file: {e}")

    print(log_entry)  # Your colored log entry for console
