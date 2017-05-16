# coding: utf-8

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
        classification = "issue"
        args = {'eventmessage':record.getMessage()}
        info = record.exc_info
        #Check if record actually has a stacktrace.
        if info is None or info.count(None) == len(info):
            info = False
            args['eventtype'] = record.name
        if record.name not in self.trakerr_client.context_tags:
            self.trakerr_client.context_tags.append(record.name)
        if (record.levelname.lower() == "debug") or (record.levelname.lower() == "info"):
            classification = "log"
        self.trakerr_client.log(args, record.levelname.lower(), classification, exc_info=info)
