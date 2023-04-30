from weeve_modules import connect, send, weeve_logger
from json import dumps
from os import path, remove
from signal import signal, SIGTERM

log = weeve_logger("processing_1_module")

output_file = "/app/artifacts/processing_1_module_report.json"

def celsius_to_fahrenheit(celsius):
    return celsius * 9/5 + 32

def main_module_logic(received_data):
    try:
        log.info(f"Received data: {received_data}")

        processed_data = received_data.copy()

        # add some data
        processed_data["temp_fahrenheit"] = celsius_to_fahrenheit(received_data["temperature"])
        processed_data["weather"] = "sunny"
        
        # send data to the next module
        resp = send(processed_data)
        log.info("Send response: %s", resp)

        # hardcode timestamp to automate data comparison in pytest functions
        resp["timestamp"] = 1.0

        # save data and response to json file
        with open(output_file, "w") as outfile:
            log.info("Saving results to output file: %s", output_file)

            output_data = {
                "received_data": received_data,
                "processed_data": processed_data,
                "send_response": resp
            }

            outfile.write(dumps(output_data))

    except Exception as e:
        log.error(f"Exception in module main logic data: {e}")

def teardown_and_exit(*args):
    del args
    if path.exists(output_file):
        remove(output_file)
    exit(0)

if __name__ == "__main__":
    signal(SIGTERM, teardown_and_exit)

    log.info("Running the first test processing module container...")

    connect(main_module_logic)
