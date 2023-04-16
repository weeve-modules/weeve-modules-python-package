# expose functions to access by the user
from weeve_modules.logger import initialize_logging, MYLogger

# initialize logging
initialize_logging()

from weeve_modules.send import send
from weeve_modules.connect import connect
from weeve_modules.connect_callback_function import set_connect_callback_function, get_connect_callback_function