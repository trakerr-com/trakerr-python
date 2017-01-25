import logging

from trakerr_handler import TrakerrHandler

class Trakerr(object):
    """description of class"""
    @classmethod
    def has_trakerr_handler(self, logger):
        """
        """
        return any([isinstance(handler, TrakerrHandler) for handler in logger.handlers])

    @classmethod
    def getLogger(self, api_key, app_version, name, url = "http://ec2-52-91-176-104.compute-1.amazonaws.com/api/v1", level = logging.ERROR, datacenter = None, datacenter_region = None):
        """
        """
        logger = logging.getLogger(name)

        if not self.has_trakerr_handler(logger):
            th = TrakerrHandler(api_key, app_version, url, level, datacenter, datacenter_region)
            logger.addHandler(th)
        return logger

