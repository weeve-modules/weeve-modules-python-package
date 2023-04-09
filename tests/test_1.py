from weeve_modules import connect, send, MYLogger
import time

log = MYLogger("test_module").getMYLogger()

log.info("Running testing script...")

def callbackMainModule(received_data):
    log.info(f"Received data: {received_data}")
    received_data["callbackNumber_timestamp"] = time.time()
    resp = send(received_data)
    log.info(f"End Callback: {resp}")

connect(callbackMainModule)
