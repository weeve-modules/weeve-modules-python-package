"""
This file sets up multithread processing of data and weeve intercontainer communication.
"""

from queue import Queue
from threading import Thread, Event
from weeve_modules import MYLogger
from weeve_modules.connect_callback_function import get_connect_callback_function

# set up logging
log = MYLogger("weeve_modules.processing_thread").getMYLogger()

class ProcessingThread(Thread):
    """
    Thread subclass for processing data received by the module.
    """
    
    def __init__(self, data_queue: Queue):
        super(ProcessingThread, self).__init__()
        self.data_queue = data_queue
        self.msg_received = Event()

    def run(self):
        """
        Runs the processing thread.
        """

        while self.msg_received.wait(timeout=None):
            while not self.data_queue.empty():
                # pass data to the module logic defined by the module developer
                try:
                    log.debug("Passing data to user defined module logic function...")
                    get_connect_callback_function()(self.data_queue.get())

                except Exception as e:
                    log.error(f"Error when passing data to user defined module logic function. {e}")
                    # break this loop that queues data as if exception happens then queue is never empty and we get infinite loop
                    break

            self.msg_received.clear()

    def resume(self):
        """
        Resumes processing thread if stopped.
        """
        self.msg_received.set()