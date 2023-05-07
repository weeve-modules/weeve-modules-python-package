from .version import __version__

# expose functions to access by the user
from .logger import initialize_logging, weeve_logger

# initialize logging
initialize_logging()

from .send import send
from .connect import connect
