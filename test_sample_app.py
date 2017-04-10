"""
    trakerr Client API

    Get your application events and errors to trakerr via the *trakerr API*.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import sys
# With handler, manual init
import logging
from trakerr import TrakerrHandler

# Normal automatic instantiation
from trakerr import Trakerr

# Without handler custom peramiters
from trakerr import TrakerrClient
from trakerr_client.models import CustomData, CustomStringData

from test.test_sample_err import ErrorTest


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
        ErrorTest.error()
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

    #Sending an error(or non-error) quickly without using the logger
    client.log({"user":"jill@trakerr.io", "session":"25", "errname":"user logon issue",
                "errmessage":"User refreshed the page."}, "info", "logon script", False)

    #Sending an error(or non-error) with custom data without the logger
    try:
        raise IndexError("Index out of bounds.")
    except:
        appevent = client.create_new_app_event("FATAL")

        # Populate any field with your own data, or send your own custom data
        appevent.context_app_browser = "Chrome"
        appevent.context_app_browser_version = "67.x"
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


if __name__ == "__main__":
    # main()
    sys.exit(main())
