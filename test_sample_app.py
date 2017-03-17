
import sys

# Normal automatic instantiation
from trakerr import Trakerr

# With handler, manual init
import logging
from trakerr import TrakerrHandler

# Without handler custom peramiters
from trakerr import TrakerrClient
from trakerr_client.models import CustomData, CustomStringData


def main(argv=None):
    """
    Main method.
    """

    if argv is None:
        argv = sys.argv

    api_key = "Api key here (or pass it in from the command line first param)"
    if len(argv) > 1:
        api_key = argv[1]
    
    #Built in python handler
    logger = Trakerr.get_logger(api_key, "1.0", "newlogger")
    try:
        error()
    except:
        logger.exception("Corrupt file.")


    # Manual instantiation of the logger.
    logger2 = logging.getLogger("Logger name")
    trakerr_handler = TrakerrHandler(api_key, "1.0")
    logger2.addHandler(trakerr_handler)

    try:
        raise ArithmeticError("2+2 is 5!")
    except:
        logger2.exception("Bad math.")


    client = TrakerrClient(api_key, "1.0", "development")

    try:
        raise IndexError("Index out of bounds.")
    except:
        appevent = client.create_new_app_event("ERROR", "Index Error")

        # Populate any field with your own data, or send your own custom data
        appevent.context_app_os = "Windows 8"
        # Can support multiple ways to input data
        appevent.custom_properties = CustomData("Custom Data holder!")
        appevent.custom_properties.string_data = CustomStringData("Custom String Data 1",
                                                                  "Custom String Data 2")
        appevent.custom_properties.string_data.custom_data3 = "More Custom Data!"
        appevent.event_user = "john@traker.io"
        appevent.event_session = "6"

        # send it to trakerr
        client.send_event_async(appevent)

    return 0


def error():
    """
    Function that reads a file.
    """
    raise EOFError("I forgot a newline!")


if __name__ == "__main__":
    # main()
    sys.exit(main())
