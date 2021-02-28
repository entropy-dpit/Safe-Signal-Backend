# Copyright (c) prisma.ai 2021
# All rights reserved

# This module logs both to the logfile and the console

__author__ = 'David Pescariu'

from datetime import datetime
import logging
from log.logger import initialize_logging

initialize_logging()

colors = {
    'note' : '\033[94m',    # Blue
    'ok'   : '\033[92m',    # Green
    'fail' : '\033[91m',    # Red
    'warn' : '\033[93m',    # Yellow

    'end'  : '\033[0m'      # Clear
}

def fatal_fail(message: str or None) -> None:
    """
    Show the fatal fail prompt

    Args:
        message (str or None): Custom message, None for blank
    """
    if message == None:
        print(f"{colors['fail']}[FATAL_FAIL] Unable to continue, exiting!{colors['end']}")
        logging.critical("[FATAL] Unable to continue, exiting!")
    else:
        print(f"{colors['fail']}[FATAL_FAIL] {message}{colors['end']}")
        logging.critical(f"[FATAL] {message}")

def fail(message: str or None) -> None:
    """
    Show the fail prompt

    Args:
        message (str or None): Custom message, None for blank
    """
    if message == None:
        print(f"{colors['warn']}[FAIL] Unknown fail{colors['end']}")
        logging.warning("Unknown fail")
    else:
        print(f"{colors['warn']}[FAIL] {message}{colors['end']}")
        logging.warning(f"{message}")

def start(rev: str) -> None:
    """
    Show the start message

    Args:
        rev (str): Current revision of the API
    """
    print(f"{colors['ok']}[START] API V3 - {rev} at {datetime.now()}{colors['end']}")
    logging.info(f"[START] API V3 - {rev} at {datetime.now()}")

def info(message: str) -> None:
    """
    Show the info message

    Args:
        message (str): The message
    """
    print(f"[INFO] {message}")
    logging.info(f"{message}")

def ok(message: str) -> None:
    """
    Show the ok message

    Args:
        message (str): The message
    """
    print(f"{colors['ok']}[OK] {message}{colors['end']}")
    logging.info(f"{message}")

def debug(message: str) -> None:
    """
    Show a debug message

    Args:
        message (str): The message
    """
    print(f"{colors['note']}[DEBUG] {message}{colors['end']}")
    logging.info(f"[RUNTIME_DEBUG] {message}")

def stop() -> None:
    """
    Show the stop message
    """
    print(f"{colors['fail']}[STOP] Stopped at {datetime.now()}{colors['end']}\n")
    logging.warning(f"[STOP] Stopped at {datetime.now()}")

def exception(exception: Exception) -> None:
    """
    Log an exception

    Args:
        exception (Exception): Exception
    """
    logging.exception(exception)
