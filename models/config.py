# Copyright (c) Team Entropy 2020
# All rights reserved

__author__ = 'David Pescariu'

import json
from os import path
from utils.console_messages import info, fatal_fail
from utils.stop_exec import stop

CONFIG_FILE_PATH = 'config/config.json'
KEY_FILE_PATH = 'config/keys.json'

class Config:
    """
    Read and store configurations
    """
    LOGGING_FORMAT      = None
    DATE_FORMAT         = None
    SERVE_PORT          = None
    ALLOW_PUBLIC        = None
    PUBLIC_UPDATE_DELAY = None

    PRIVATE_KEYS        = {}
    PUBLIC_KEYS         = {}

    DB_LOGIN_USER       = None
    DB_LOGIN_PASS       = None

    def __do_config_files_exist(self) -> bool:
        """
        Checks if the config and key files exist

        Returns:
            bool: True - they exist | False - they do not exist
        """
        if not path.exists(CONFIG_FILE_PATH): 
            info("Couldn't find config.json!")
            return False
        if not path.exists(KEY_FILE_PATH): 
            info("Couldn't find keys.json!")
            return False
        return True

    def __init__(self):
        if not self.__do_config_files_exist():
            fatal_fail("One or more required files not found!")
            stop()
        # Load config
        with open(CONFIG_FILE_PATH) as conf_file:
            json_ = json.load(conf_file)
            self.LOGGING_FORMAT = json_["logging_format"]
            self.DATE_FORMAT = json_["date_format"]
            self.SERVE_PORT = json_["serve_port"]
            self.ALLOW_PUBLIC = json_["allow_public"]
            self.PUBLIC_UPDATE_DELAY = json_["public_update_delay"]
        info("Configs loaded")
        # Load keys
        with open(KEY_FILE_PATH) as key_file:
            json_ = json.load(key_file)
            private_keys = json_["private_keys"]
            public_keys = json_["public_keys"]

            for key in private_keys:
                self.PRIVATE_KEYS[key] = "valid"
            for key in public_keys:
                self.PUBLIC_KEYS[key] = "valid"

            self.DB_LOGIN_USER = json_["db_user"]
            self.DB_LOGIN_PASS = json_["db_pass"]
        info("Keys loaded")