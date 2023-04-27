# expose functions to access by the user
from weeve_modules.logger import initialize_logging, weeve_logger

# initialize logging
initialize_logging()

from weeve_modules.send import send
from weeve_modules.connect import connect