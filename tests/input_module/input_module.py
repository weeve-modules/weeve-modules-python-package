from weeve_modules import send, weeve_logger
from bottle import run, post, request
from json import dumps
from os import path, remove
from signal import signal, SIGTERM

log = weeve_logger("input_module")

output_file = "/app/artifacts/input_module_report.json"

@post("/")
def request_handler():
    try:
        received_data = request.json
        log.info("Received data: %s", received_data)

        # send data to the next module
        resp = send(received_data)
        log.info("Send response: %s", resp)

        # hardcode timestamp to automate data comparison in pytest functions
        resp["timestamp"] = 0.0

        # save data and response to json file
        with open(output_file, "w") as outfile:
            log.info("Saving results to output file: %s", output_file)

            output_data = {
                "received_data": received_data,
                "send_response": resp
            }

            outfile.write(dumps(output_data))

        return "OK"

    except Exception as e:
        return f"Exception when receiving data: {e}"

def teardown_and_exit(*args):
    del args
    if path.exists(output_file):
        remove(output_file)
    exit(0)

if __name__ == "__main__":
    signal(SIGTERM, teardown_and_exit)

    log.info("Running test input module container on 0.0.0.0 port 8080")

    # start the server
    run(
        host="0.0.0.0",
        port=8080,
        quiet=True,
    )
