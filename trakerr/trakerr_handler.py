import logging
from trakerr_IO import TrakerrClient
from trakerr_utils import TrakerrUtils

class TrakerrHandler(logging.Handler):
    """description of class"""

    def __init__(self, api_key, app_version, context_env_name = None, 
                 context_env_version = None, context_env_hostname = None,
                 context_appos = None, context_appos_version = None,
                 datacenter = None, datacenter_region = None,
                 client = None, url = TrakerrUtils.SERVER_URL,  level = logging.ERROR):
        """
        Ether client or the args after clients must be not none.
        """
        logging.Handler.__init__(self, level = level)

        if isinstance(client, TrakerrClient):
            self.trakerr_client = client
        else:
            self.trakerr_client = TrakerrClient(api_key, app_version, context_env_name, context_env_version, context_env_hostname,
                                                context_appos, context_appos_version, datacenter, datacenter_region, url)

    def emit(self, record):
        """
        """
        self.trakerr_client.log(record.levelname, error_message = record.getMessage(), exc_info = record.exc_info)

    def format_record(self, record):#Might not need.
        raise NotImplementedError