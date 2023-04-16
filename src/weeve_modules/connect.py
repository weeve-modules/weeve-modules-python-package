from os import getenv
from bottle import run
from weeve_modules import MYLogger
from weeve_modules.request_handler import request_handler
from weeve_modules.connect_callback_function import set_connect_callback_function

# set up logging
log = MYLogger("weeve_modules.connect").getMYLogger()

def connect(callback_function: object):
    """
    Connect to weeve intercontainer communication and save a user defined callback function where received data by this module is passed for further processing.

    Args:
        callback_function (object): The callback function defined by a user and ready to received data for further processing.
    """

    set_connect_callback_function(callback_function)

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
