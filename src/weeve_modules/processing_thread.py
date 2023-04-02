"""
This file sets up multithread processing of data and weeve intercontainer communication.
"""

from queue import Queue
from threading import Thread, Event
from weeve_modules import Logger
from weeve_modules.connect import getConnectCallbackFunction

# set up logging
log = Logger("weeve_modules.processing_thread")

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
                    getConnectCallbackFunction(self.data_queue.get())
                    log.debug("Passed data to user defined module logic function.")

                except Exception as e:
                    log.error(f"Error when passing data to user defined module logic function. {e}")

            self.msg_received.clear()

    def resume(self):
        """
        Resumes processing thread if stopped.
        """
        self.msg_received.set()