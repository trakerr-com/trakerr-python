import logging
import platform

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
    def getLogger(self, api_key,  app_version, name, context_env_name = "development", 
                 context_env_version = platform.python_implementation()+ " " + platform.python_version(), context_env_hostname = platform.node(),
                 context_appos = platform.system() + " " + platform.release(), context_appos_version = platform.version(),
                 datacenter = None, datacenter_region = None,
                 client = None, url = TrakerrUtils.SERVER_URL,  level = logging.ERROR):
        """
        """
        logger = logging.getLogger(str(name))

        if not Trakerr.has_trakerr_handler(logger):
            th = TrakerrHandler(api_key, app_version, context_env_name, context_env_version, context_env_hostname,
                                context_appos, context_appos_version, datacenter, datacenter_region, client, url, level)
            logger.addHandler(th)
        return logger