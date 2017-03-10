"""
    Trakerr Client API

    Get your application events and errors to Trakerr via the *Trakerr API*.

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

"""
#Normal automatic instantiation
from trakerr import Trakerr
"""

"""
#With handler, manual init
import logging
from trakerr import TrakerrHandler
"""


# Without handler custom peramiters
from trakerr import TrakerrClient
from trakerr_client.models import CustomData, CustomStringData


def main(argv=None):
    """
    Main method.
    """
    """
    if argv is None:
        argv = sys.argv

    logger = Trakerr.getLogger("ca6b942a89e04069ec96fa2b3438efb310995233724595", "1.0", "newlogger")
    try:
        error()
    except:
        logger.exception("Bad math.")
    """

    """
    #Manual instantiation of the logger.
    logger = logging.getLogger("Logger name")
    th = TrakerrHandler("API KEY", "App Version number here")
    logger.addHandler(th)

    try:
        raise ArithmeticError()
    except:
       logger.exception("Bad math.")

    """

    client = TrakerrClient(
        "ca6b942a89e04069ec96fa2b3438efb310995233724595", "1.0")

    try:
        raise IndexError("Bad Math")
    except:
        appevent = client.create_new_app_event_error(
            "ERROR", "Index Error", "Math")
        #appevent = client.create_new_app_event("ERROR", "Index Error", "Math")
        # You can use this call to create an app event without a stacktrace,
        # in case you do don't have a stacktrace or you're not sending a crash.

        # Populate any field with your own data, or send your own custom data
        appevent.context_app_os = "Windows 8"
        appevent.custom_properties = CustomData("Custom Data holder!")

        # Can support multiple ways to insert.
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
    Oh no!
    """
    raise EOFError()


if __name__ == "__main__":
    # main()
    sys.exit(main())
