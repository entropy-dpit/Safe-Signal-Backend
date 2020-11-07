# Copyright (c) Team Entropy 2020
# All rights reserved

__author__ = 'David Pescariu'

import importlib
from utils.console_messages import fail

REQUIRED_MODULES = [
    "sys",
    "os",
    "logging",
    "datetime",
    "enum",
    "json",
    "flask",
    "waitress",
    "mysql.connector"
]


def check_imports() -> bool:
    """
    Checks to see if all modules can be imported.
    Prints any module that wasn't found.

    Returns:
        Boolean: True if a module(or more) wasn't found, False if all found
    """    
    anyNotFound = False

    for module in REQUIRED_MODULES:
        spec = importlib.util.find_spec(module)
        wasFound = spec is not None
        if not wasFound:
            fail(f"Module {module} was not found!")
            #TODO: Add logger
            anyNotFound = True

    return anyNotFound

# EOF
