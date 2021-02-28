# Copyright (c) prisma.ai
# License: GNU GPL v3

# Public Release - 7 Nov 2020 / Updated Feb 2021

__author__ = 'David Pescariu'

import logging
import utils.check_imports as check_imports_
import utils.console_messages as msg
import utils.stop_exec as stop
import api.serve_api as api
import api.cleanup as cleanup
from models.config import Config
from log.logger import initialize_logging

REV = "Rev-8.19"

def main():
    msg.start(REV)
    msg.info("Initializing...")
    
    # Load configs
    config = Config()
    initialize_logging()
    msg.info("Checking for missing modules")
    
    if check_imports_.check_imports():
        # Fatal -> One or more modules not found
        msg.fatal_fail("One or more modules not found")
        logging.critical("One or more modules not found -> exiting")
        stop.stop()
    else:
        msg.ok("All modules found")
    
    msg.ok("Successfully initialized, start serving:")
    msg.info("Ctrl-C to Stop Serving")
    api.start_serving(config)
    
    cleanup.cleanup()

if __name__ == "__main__":
    main()