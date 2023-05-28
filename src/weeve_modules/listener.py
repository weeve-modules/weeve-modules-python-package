"""
This file implements a mechanism that enables the module developer to set up listener server to receive data from other module within weeve intercontainer communication.
"""

import sys
from os import getenv
from bottle import run
from weeve_modules.logger import weeve_logger
from weeve_modules.request_handler import request_handler
from weeve_modules.listener_callback_function import set_listener_callback_function

# set up logging
log = weeve_logger("weeve_modules.listener")

def listener(callback_function: object = None) -> None:
    """
    Set up a listener to weeve intercontainer communication and save a user defined callback function where received data by this module is passed to for further processing.

    Args:
        callback_function (object): The callback function defined by a user and ready to receive data for further processing. Callback function must accept data as an argument.
    """

    log.info(
        "%s running on %s at port %s with end-point set to %s",
        getenv("WEEVE_MODULE_NAME"),
        getenv("WEEVE_INGRESS_HOST"),
        getenv("WEEVE_INGRESS_PORT"),
        getenv("WEEVE_EGRESS_URLS")
    )

    if not callback_function:
        sys.exit("Error: callback_function is None. Please provide a valid callback function argument.")

    set_listener_callback_function(callback_function)

    # start the server
    run(
        host=getenv("WEEVE_INGRESS_HOST"),
        port=getenv("WEEVE_INGRESS_PORT"),
        quiet=True
    )
