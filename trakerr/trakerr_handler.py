import logging
from trakerr_io import TrakerrClient
from trakerr_utils import TrakerrUtils

class TrakerrHandler(logging.Handler):
    """
    Class that extends logging.Handler to provide its own implementation of emit.
    """

    def __init__(self, api_key, app_version, context_deployment_name=None,
                 client=None, level=logging.ERROR):
        """
        Ether client or the args after clients must be not none.
        """
        logging.Handler.__init__(self, level=level)

        if isinstance(client, TrakerrClient):
            self.trakerr_client = client
        else:
            self.trakerr_client = TrakerrClient(
                api_key, app_version, context_deployment_name)

    def emit(self, record):
        """
        Overload emit to send to trakerr.
        :param record: Record object returned by the super handl
        """
        self.trakerr_client.log({'errmessage': record.getMessage()},
                                record.levelname.lower(), exc_info=record.exc_info)
