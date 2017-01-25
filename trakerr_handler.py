import logging
from trakerr__client import TrakerrSend

class TrakerrHandler(logging.Handler):
    """description of class"""

    def __init__(self, api_key,  app_version, url = "http://ec2-52-91-176-104.compute-1.amazonaws.com/api/v1", level = logging.ERROR, datacenter = None, datacenter_region = None, client = None):
        """
        Ether client or the args after clients must be not none.
        """
        logging.Handler.__init__(self, level = level)

        if isinstance(client, TrakerrSend):
            self.trakerr_client = client
        else:
            self.trakerr_client = TrakerrSend(api_key, url, app_version, datacenter, datacenter_region)

    def emit(self, record):
        """
        """
        self.trakerr_client.log(record.levelname, error_message = record.msg, exc_info = record.exc_info)

    def format_record(self, record):#Might not need.
        raise NotImplementedError