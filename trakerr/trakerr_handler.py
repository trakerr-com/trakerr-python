﻿
import logging
from trakerr.trakerr_io import TrakerrClient

class TrakerrHandler(logging.Handler):
    """
    Class that extends logging.Handler to provide its own implementation of emit.
    """

    def __init__(self, api_key=None, app_version="1.0", context_deployment_stage="deployment",
                 client=None, level=logging.WARNING):
        """
        Ether client or the args after clients must be not none.
        :param string api_key: The API key on trakerr.
        :param string app_version: The version your codebase is on.
        :param string context_deployment_stage: The deployment stage your codebase is on
                                              (production, development, test).
        :param TrakerrClient client: Optional parameter to provide a TrakerrClient instance,
                                    if you would have liked to have changed default values.
        :param logging.SEVERITY level: Optional parameter to set the level of error the handler is triggered by.
                                      The default value is Warning and above. DEBUG logs all events debug and above.
                                      See the python logger docs for full enum values and creating custom values.
        """
        super(TrakerrHandler, self).__init__(level=level)

        if isinstance(client, TrakerrClient):
            self.trakerr_client = client
        else:
            self.trakerr_client = TrakerrClient(
                api_key, app_version, context_deployment_stage)

    def emit(self, record):
        """
        Overload emit to send to trakerr.
        :param record: Record object returned by the super handler.
        """
        #Check if record actually has a stacktrace.
        info = record.exc_info
        if info is None or info.count(None) == len(info):
            info = False
        args = {'eventmessage':record.getMessage(), 'tags':[record.name]}
        classification = "issue"
        if (record.levelname.lower() == "debug") or (record.levelname.lower() == "info"):
            args['eventtype'] = record.name
            classification = "log"
        self.trakerr_client.log(args, record.levelname.lower(), classification, exc_info=info)
