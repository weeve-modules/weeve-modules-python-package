from weeve_modules import connect, send, weeve_logger
from json import dumps
from os import path, remove
from signal import signal, SIGTERM

log = weeve_logger("processing_2_module")

output_file = "/app/artifacts/processing_2_module_report.json"

def main_module_logic(received_data):
    try:
        log.info(f"Received data: {received_data}")

        processed_data = received_data.copy()

        # add some data
        processed_data["voltage"] = 215.23
        processed_data["altitude"] = 2405
        processed_data["warnings"] = True
        
        # send data to the next module
        resp = send(processed_data)
        log.info("Send response: %s", resp)

        if resp["status_code"] == 400:
            # change the error message erronous object memory location to be compatible with ground truth test as it is assigned randomly by the system
            in_string_memory_address_location = resp["message"].find("object at")
            if in_string_memory_address_location > -1:
                # remove memory address
                resp["message"] = resp["message"].replace(resp["message"][in_string_memory_address_location+10:resp["message"].find(">", in_string_memory_address_location+10)],"")

        # hardcode timestamp to automate data comparison in pytest functions
        resp["timestamp"] = 2.0

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
    # if path.exists(output_file):
    #     remove(output_file)
    exit(0)

if __name__ == "__main__":
    signal(SIGTERM, teardown_and_exit)

    log.info("Running the second test processing module container...")

    connect(main_module_logic)
