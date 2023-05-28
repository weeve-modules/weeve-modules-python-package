"""
This file implements output aspect of the module's intercontainer communication.
It sends data over REST API POST method to the next module in the edge application.
"""

from os import getenv
from requests import exceptions, post
from weeve_modules.logger import weeve_logger
import time

log = weeve_logger("weeve_modules.send")

def send(processed_data: any) -> dict:
    """
    Send processed data to the next module in weeve Edge Application.

    Args:
        processed_data (any): processed data to send to the next module.

    Returns:
        dict: custom response dict in format 
                {
                    "status_code": 200 for success and 400 otherwise, 
                    "ok": True if successfully sent data and False otherwise,
                    "message": Success or error message,
                    "timestamp": Timestamp when sent or attempted to send data.
                }
    """

    try:
        # parse egress urls for fanout
        urls = [url.strip() for url in getenv("WEEVE_EGRESS_URLS").strip(",").split(",")]

        # for collecting REST API POST responses
        failed_responses = []

        # fan-out
        for url in urls:
            # send data to the next module
            sending_timestamp = time.time()
            response = post(url=url, json=processed_data)

            if response.status_code != 200:
                # on sending error
                log.debug(f"Failed sending data to {url} | Response: {response.status_code} {response.reason}")
                
                failed_responses.append(
                    {
                        "url": url,
                        "status_code": response.status_code,
                        "message": response.text,
                        "timestamp": sending_timestamp
                    }
                )
            else: 
                # on sending success
                log.debug(f"Successfully sent data to url {url} | Response: {response.status_code} {response.reason}")

        if failed_responses:
            # info on failed responses
            return {
                    "status_code": 400,
                    "ok": False,
                    "message": f"Failed sending data to the following egress urls: {failed_responses}",
                    "timestamp": time.time()
                }

        return {
                "status_code": 200,
                "ok": True,
                "message": "Successfully sent data to the next module.",
                "timestamp": sending_timestamp
            }

    except (
        exceptions.RequestException,
        exceptions.ConnectionError,
        exceptions.ConnectTimeout,
    ) as e:
        return {
                "status_code": 400,
                "ok": False,
                "message": f"Exception when sending data to the next module: {e}",
                "timestamp": time.time()
            }