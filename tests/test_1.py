from weeve_modules import connect, send, weeve_logger
import time

log = weeve_logger("test_module")

log.info("Running testing script...")

def callbackMainModule(received_data):
    log.info(f"Received data: {received_data}")
    received_data["callbackNumber_timestamp"] = time.time()
    resp = send(received_data)
    log.info(f"End Callback: {resp}")

connect(callbackMainModule)
