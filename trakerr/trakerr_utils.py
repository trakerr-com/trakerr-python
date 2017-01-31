import sys
import os
import re
import traceback

class TrakerrUtils(object):

    SERVER_URL = "http://ec2-52-91-176-104.compute-1.amazonaws.com/api/v1"

    @classmethod
    def format_error_name(self, error_type):
        """
        Takes in a type object and returns a string "package.typename." It will stringify the type object if it cannot find find the expression.

        :param error_type: The type object to extract the string.

        :return: A string with either the found string or a string representation of the type object if it cannot find the patern above.
        """

        name = str(error_type)
        rules = re.compile(r"\w+\.\w+", re.IGNORECASE)
        found = rules.findall(name)
        if len(found) > 0: name = found[0]

        return name

    @classmethod
    def is_exc_info_tuple(self, exc_info):
        """
        """

        raise NotImplementedError("Method not implemented currently.")