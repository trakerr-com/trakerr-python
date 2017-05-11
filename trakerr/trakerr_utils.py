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

import re
import types


class TrakerrUtils(object):
    """
    Collection of utility methods to be used in the API.
    """

    @classmethod
    def format_error_name(cls, error_type):
        """
        Takes in a type object and returns a string "package.typename."
        It will stringify the type object if it cannot find find the expression.
        :param error_type: The type object to extract the string.
        :return: A string with either the found string,
         or a string representation of the type object if it cannot find the patern above.
        """

        name = str(error_type)
        rules = re.compile(r"\w+\.\w+", re.IGNORECASE)
        found = rules.findall(name)
        if len(found) > 0:
            name = found[0]

        return name

    @classmethod
    def is_exc_info_tuple(cls, exc_info):
        """
        Checks if the passed exc_info is an exc info tuple.
        :param exc_info: The item to check for exc_info.
        :return: A boolean value on if it is or isn't an exc info tuple.
        """

        try:
            errtype, value, tback = exc_info
            if all([x is None for x in exc_info]):
                return True
            elif all((isinstance(errtype, type),
                      isinstance(value, Exception),
                      hasattr(tback, 'tb_frame'),
                      hasattr(tback, 'tb_lineno'),
                      hasattr(tback, 'tb_next'))):
                return True
        except (TypeError, ValueError):
            pass

        return False
