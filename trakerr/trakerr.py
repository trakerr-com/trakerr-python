import logging

from trakerr_handler import TrakerrHandler
from trakerr_utils import TrakerrUtils

class Trakerr(object):
    """
    description of class
    """

    @classmethod
    def has_trakerr_handler(self, logger):
        """
        """
        return any([isinstance(handler, TrakerrHandler) for handler in logger.handlers])

    @classmethod
    def getLogger(self, api_key, app_version, name, url = TrakerrUtils.SERVER_URL, level = logging.ERROR, datacenter = None, datacenter_region = None):
        """
        """
        logger = logging.getLogger(name)

        if not Trakerr.has_trakerr_handler(logger):
            th = TrakerrHandler(api_key, app_version, url, level, datacenter, datacenter_region)
            logger.addHandler(th)
        return logger