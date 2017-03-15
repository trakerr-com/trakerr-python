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

from trakerr_handler import TrakerrHandler

class Trakerr(object):
    """
    An external facing class that provides static methods for creating a TrakerrHandler.
    """

    @classmethod
    def has_trakerr_handler(cls, logger):
        """
        checks to see if a logger handler instance
        has already been registered with the global logger.
        :param logger: The logger instance to look for.
        :return: A logger handler instance with the same name as the logger we are looking for.
        """
        return any([isinstance(handler, TrakerrHandler) for handler in logger.handlers])

    @classmethod
    def get_logger(cls, api_key, app_version, name, context_development_stage="development"):
        """
        Instantiate a logger instance and add a trakerr extended handler to it.
        :param api_key: String apikey of your trakerr application.
        :param app_version: String app version of your  application
        :param name: String name of the logger being created or attached to.
        :param context_env_name: String staging name of the current codebase of your application.
        :return: A logger instance with a Trakerr handler added to it.
        """
        logger = logging.getLogger(str(name))

        if not Trakerr.has_trakerr_handler(logger):
            trakerr_handler = TrakerrHandler(api_key, app_version, context_development_stage)
            logger.addHandler(trakerr_handler)
        return logger
