# Copyright (c) Team Entropy 2020
# All rights reserved

__author__ = 'David Pescariu'

import utils.console_messages as msg
import utils.stop_exec as stop

def cleanup() -> None:
    """
    Run cleanup
    """
    msg.info("Cleaning up")
    stop.stop()
