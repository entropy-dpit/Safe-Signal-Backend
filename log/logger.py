# Copyright (c) Team Entropy 2020
# All rights reserved

__author__ = 'David Pescariu'

import logging

def initialize_logging():
    logging.basicConfig(
        filename='log/api_log.log', 
        level='INFO', 
        format="%(asctime)s - %(name)s [%(levelname)s] %(message)s", 
        )
