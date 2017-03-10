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

import logging
from trakerr_io import TrakerrClient
from trakerr_utils import TrakerrUtils


class TrakerrHandler(logging.Handler):
    """
    This class inherits TrakerrHandler to take in created records and sends it out.
    """

    def __init__(self, api_key, app_version, context_env_name=None,
                 context_env_version=None, context_env_hostname=None,
                 context_appos=None, context_appos_version=None,
                 datacenter=None, datacenter_region=None,
                 client=None, url=TrakerrUtils.SERVER_URL, level=logging.ERROR):
        """
        Initializes the handler.
        """
        logging.Handler.__init__(self, level=level)

        if isinstance(client, TrakerrClient):
            self.trakerr_client = client
        else:
            self.trakerr_client = TrakerrClient(api_key, app_version, context_env_name,
                                                context_env_version, context_env_hostname,
                                                context_appos, context_appos_version,
                                                datacenter, datacenter_region, url)

    def emit(self, record):
        """
        Logs the record with Trakerr.
        :param record: The record compiled by the exception handler
        """
        self.trakerr_client.log(
            record.levelname, error_message=record.getMessage(), exc_info=record.exc_info)
