import logging
import platform

from trakerr_handler import TrakerrHandler
from trakerr_utils import TrakerrUtils


class Trakerr(object):
    """
    description of class
    """

    @classmethod
    def has_trakerr_handler(cls, logger):
        """
        """
        return any([isinstance(handler, TrakerrHandler) for handler in logger.handlers])

    @classmethod
    def get_logger(cls, api_key, app_version, name, context_env_name="development"):
        """
        """
        logger = logging.getLogger(str(name))

        if not Trakerr.has_trakerr_handler(logger):
            th_ = TrakerrHandler(api_key, app_version, context_env_name)
            logger.addHandler(th_)
        return logger
