from os import getenv
from bottle import run
from weeve_modules import MYLogger
from weeve_modules.request_handler import request_handler

# set up logging
log = MYLogger("weeve_modules.connect").getMYLogger()

CONNECT_CALLBACK_FUNCTION = None

def connect(callback_function: object):
    """
    Connect to weeve intercontainer communication and save a user defined callback function where received data by this module is passed for further processing.

    Args:
        callback_function (object): The callback function defined by a user and ready to received data for further processing.
    """

    global CONNECT_CALLBACK_FUNCTION 
    CONNECT_CALLBACK_FUNCTION = callback_function

    log.info(
        "%s running on %s at port %s with end-point set to %s",
        getenv("MODULE_NAME"),
        getenv("INGRESS_HOST"),
        getenv("INGRESS_PORT"),
        getenv("EGRESS_URLS"),
    )

    # start the server
    run(
        host=getenv("INGRESS_HOST"),
        port=getenv("INGRESS_PORT"),
        quiet=True,
    )

def getConnectCallbackFunction() -> object:
    """
    Returns:
        object: The callback function defined by a user where received data is passed for further processing.
    """
    
    return CONNECT_CALLBACK_FUNCTION
