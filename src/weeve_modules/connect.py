"""
This file implements a mechanism that enables the module developer to connect to weeve intercontainer communication.
"""

import sys
from os import getenv
from signal import signal, SIGTERM
from bottle import run
from weeve_modules.logger import weeve_logger
from weeve_modules.request_handler import request_handler
from weeve_modules.connect_callback_function import set_connect_callback_function

# set up logging
log = weeve_logger("weeve_modules.connect")

def gracefully_terminate(*args):
    """
    Gracefully terminate the module script.
    """
    del args
    sys.exit("Successfully terminated the module.")

def connect(callback_function: object = None, input_module: bool = False, gracefully_terminate: bool = True) -> None:
    """
    Connect to weeve intercontainer communication and save a user defined callback function where received data by this module is passed to for further processing.

    Args:
        callback_function (object): The callback function defined by a user and ready to received data for further processing.
        input_module (bool): Flag whether the module is Input module or not. If true, then it does not require callback_function argument. 
        gracefully_terminate (bool): (Optional) Whether to gracefully terminate the module container. This is optional as developers might want to implement their own graceful termination if their modules use extra resources or files.
    """

    # graceful termination
    if gracefully_terminate:
        # Docker by default sends a SIGTERM to a container and waits 10 seconds for it to stop before killing it with a SIGKILL
        signal(SIGTERM, gracefully_terminate)

    if not input_module:
        # set up Processing and Output Modules

        log.info(
            "%s running on %s at port %s with end-point set to %s",
            getenv("WEEVE_MODULE_NAME"),
            getenv("WEEVE_INGRESS_HOST"),
            getenv("WEEVE_INGRESS_PORT"),
            getenv("WEEVE_EGRESS_URLS"),
        )

        if not callback_function:
            sys.exit("Error: callback_function is None. Please provide a valid callback function argument.")

        set_connect_callback_function(callback_function)

        # start the server
        run(
            host=getenv("WEEVE_INGRESS_HOST"),
            port=getenv("WEEVE_INGRESS_PORT"),
            quiet=True,
        )
        
    else:
        # set up Input Module

        log.info(
            "%s running with end-point set to %s",
            getenv("WEEVE_MODULE_NAME"),
            getenv("WEEVE_EGRESS_URLS"),
        )
