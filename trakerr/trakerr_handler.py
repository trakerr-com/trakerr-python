import logging
from trakerr_IO import TrakerrClient
from trakerr_utils import TrakerrUtils

class TrakerrHandler(logging.Handler):
    """description of class"""

    def __init__(self, api_key, app_version, context_env_name=None,
                 client=None, level=logging.ERROR):
        """
        Ether client or the args after clients must be not none.
        """
        logging.Handler.__init__(self, level = level)

        if isinstance(client, TrakerrClient):
            self.trakerr_client = client
        else:
            self.trakerr_client = TrakerrClient(
                api_key, app_version, context_env_name)

    def emit(self, record):
        """
        """
        self.trakerr_client.log({'errmessage': record.getMessage()},
                                record.levelname, record.exc_info)