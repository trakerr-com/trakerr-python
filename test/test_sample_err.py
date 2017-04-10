"""
    trakerr Client API

    Get your application events and errors to trakerr via the *trakerr API*.

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

class ErrorTest(object):
    """
    A class that throws an error.
    """
    @classmethod
    def _level_one(cls):
        """
        throws an error at a level below normal.
        """
        raise EOFError("I forgot a newline!")

    @classmethod
    def error(cls):
        """
        Function that reads a file.
        """
        cls._level_one()
