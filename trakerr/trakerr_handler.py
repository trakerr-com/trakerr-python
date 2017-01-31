import logging
from trakerr_IO import TrakerrIO
from trakerr_utils import TrakerrUtils

class TrakerrHandler(logging.Handler):
    """description of class"""

    def __init__(self, api_key,  app_version, url = TrakerrUtils.SERVER_URL, level = logging.ERROR, datacenter = None, datacenter_region = None, client = None):
        """
        Ether client or the args after clients must be not none.
        """
        logging.Handler.__init__(self, level = level)

        if isinstance(client, TrakerrIO):
            self.trakerr_client = client
        else:
            self.trakerr_client = TrakerrIO(api_key, app_version, url, datacenter, datacenter_region)

    def emit(self, record):
        """
        """
        self.trakerr_client.log(record.levelname, error_message = record.msg, exc_info = record.exc_info)

    def format_record(self, record):#Might not need.
        raise NotImplementedError