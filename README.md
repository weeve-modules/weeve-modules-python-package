# weeve Modules Python Package

This Python pip package is a specially designed support package for developers to implement their own weeve modules.
The package takes care of all weeve specific intercontainer communication protocols and other aspects of the module's functionality within weeve ecosystem.

For the full documentation on building weeve modules, please see our official docs: [How to create a weeve module](https://docs.weeve.engineering/guides/how-to-create-a-weeve-module).

- [weeve Modules Python Package](#weeve-modules-python-package)
  - [Package specific environment variables](#package-specific-environment-variables)
  - [weeve\_modules.connect()](#weeve_modulesconnect)
  - [weeve\_modules.send()](#weeve_modulessend)
  - [weeve\_modules.weeve\_logger()](#weeve_modulesweeve_logger)
  - [Example: Input Module](#example-input-module)
  - [Example: Processing Module](#example-processing-module)
  - [Example: Output Module](#example-output-module)

## Package specific environment variables

These environment variables are set by the weeve Agent on the edge-node. In order to avoid conflicts, do not override these environments when pushing modules to production (use them for dev and testing only).

| Environment Variables | type   | Description                                                                                                                                                                 |
| --------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| WEEVE_LOG_LEVEL       | string | Allowed log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Refer to [logging levels package documentation](https://docs.python.org/3/library/logging.html#levels). |
| WEEVE_MODULE_NAME     | string | Name of the module.                                                                                                                                                         |
| WEEVE_INGRESS_HOST    | string | Host to which data will be received.                                                                                                                                        |
| WEEVE_INGRESS_PORT    | string | Port to which data will be received.                                                                                                                                        |
| WEEVE_EGRESS_URLS     | string | HTTP ReST endpoint for the next modules.                                                                                                                                    |


## weeve_modules.connect()

`connect()` is the most important function as it allows the module to connect to weeve ecosystem in production. `connect()` takes three arguments:

* `callback_function` (`object`): The callback function defined by a user and ready to receive data for further processing. Callback function **must** accept data as an argument.
* `input_module` (`bool`): Flag whether the module is Input module or not. If `True`, then it does not require callback_function argument. 
* `gracefully_terminate` (`bool`): (Optional) Whether to gracefully terminate the module container. This is optional as developers might want to implement their own graceful termination if their modules use extra resources or files. We strongly recommend setting `gracefully_terminate` to `True` unless the module uses volumes, external resources, etc. when the custom implementation of graceful termination might be required.

```python
from weeve_modules import connect

def my_module_logic(data):
    # yout module code here

if __name__ == "__main__":
    connect(callback_function=my_module_logic, input_module=True, gracefully_terminate=True)
```

## weeve_modules.send()

This function enables passing data to the next module in the weeve Edge Application. It takes only one argument:

* `processed_data` (`any`): Data to send to the next module.

It returns a custom response dictionary:

```text
{
    "status_code": 200 for success and 400 otherwise, 
    "ok": True if successfully sent data and False otherwise,
    "message": Success or error message,
    "timestamp": Timestamp when sent or attempted to send data.
}
```

Example:

```python
from weeve_modules import send

# send data to the next module
resp = send({"temperature": 12, "pressure": 1019})
if resp.status_code == 400:
    # your error protocol
```

## weeve_modules.weeve_logger()

Weeve logger is based on [logging package](https://docs.python.org/3/library/logging.html#). There are five supported logging levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Refer to [logging levels package documentation](https://docs.python.org/3/library/logging.html#levels). These messages have a custom weeve logging protocol which is in sync with weeve Agent and API. Current schema:

```text
{
    "timestamp": <timestamp>,
    "level": <logging_level>,
    "filename": <log_message_source_filename>,
    "message": <log_message>
}
```

Example:

```python
from weeve_modules import weeve_logger

# initialize logging by providing logger name, we strongly recommend using the filename
log = weeve_logger("tutorial_module")

# logging examples
log.debug("This is debug log messege.")
log.info("This is info log messege.")
log.warning("This is warning log messege.")
log.error("This is error log messege.")
log.critical("This is critical log messege.")
```

## Example: Input Module

This is an example of a simple input module that receives data over HTTP ReST and passes it to the next module in the weeve Edge Application.
We need `send()`, `weeve_logger()` and `connect()` functions.

```python
from weeve_modules import send, weeve_logger, connect
from bottle import run, post, request

log = weeve_logger("my_input_module")

@post("/")
def request_handler():
    # receive data
    received_data = request.json
    
    # send data to the next module
    resp = send(received_data)

if __name__ == "__main__":
    # connect to weeve ecosystem
    connect(callback_function=None, input_module=True, gracefully_terminate=True)

    # start the server on http://0.0.0.0:8080/
    run(
        host="0.0.0.0",
        port=8080,
        quiet=True,
    )
```

## Example: Processing Module

This is an example of a simple processing module that receives data from the previous module and filters out `temperature` lower that 0. Later it sends data to the next module in the weeve Edge Application.
We need `send()`, `weeve_logger()` and `connect()` functions.

```python
from weeve_modules import send, weeve_logger, connect

log = weeve_logger("my_processing_module")

# my module logic functionality
def filter_temperature(data):

    # filter temperature data
    if data["temperature"] >= 0:

        # send data to the next module 
        resp = send(data)
        
        # check the success of sending the data
        if resp.status_code == 200:
            log.info("Successfully passed filetered data.")
        else:
            log.error("Failed to pass filetered data: %s", resp.message)

if __name__ == "__main__":

    # connect to weeve ecosystem
    connect(callback_function=filter_temperature, input_module=False, gracefully_terminate=True)
```

## Example: Output Module

This is an example of a simple output module that receives data from the previous module and sends it over HTTP ReST to a selected endpoint.
We need `weeve_logger()` and `connect()` functions.

```python
from weeve_modules import weeve_logger, connect
from requests import post
from json import dumps

log = weeve_logger("my_output_module")

# my module logic functionality
def send_to_endpoint(data):

    log.info("Sending data to the endpoint.")
    post(url="", json=data)

if __name__ == "__main__":
    
    # connect to weeve ecosystem
    connect(callback_function=send_to_endpoint, input_module=False, gracefully_terminate=True)
```
