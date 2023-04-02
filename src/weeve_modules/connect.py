CONNECT_CALLBACK_FUNCTION = None

def connect(callback_function: object):
    """
    This function saves a user defined callback function where data, which is received by this module, is passed for further processing.

    Args:
        callback_function (object): The callback function defined by a user and ready to received data for further processing.
    """

    global CONNECT_CALLBACK_FUNCTION 
    CONNECT_CALLBACK_FUNCTION = callback_function

def getConnectCallbackFunction() -> object:
    """
    Returns:
        object: The callback function defined by a user where received data is passed for further processing.
    """
    
    return CONNECT_CALLBACK_FUNCTION
