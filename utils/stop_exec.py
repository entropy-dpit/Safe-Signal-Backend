# Copyright (c) prisma.ai 2021
# All rights reserved

__author__ = 'David Pescariu'

from utils.console_messages import stop as stop_msg

def stop() -> None:
    """
    Stop execution and display the stop message
    """
    stop_msg()
    quit()
