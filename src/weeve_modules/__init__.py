from .version import __weeve_sdk_version__

# expose functions to access by the user
from .logger import initialize_logging, weeve_logger

# initialize logging
initialize_logging()

# initialize HTTP POST endpoint for incoming data
from weeve_modules.request_handler import request_handler

from .send import send
from .listener import listener
from .add_graceful_termination import add_graceful_termination
