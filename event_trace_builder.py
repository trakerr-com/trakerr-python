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


from __future__ import absolute_import #Only seems to matter in py 2.5? http://stackoverflow.com/questions/33743880/what-does-from-future-import-absolute-import-actually-do
from __builtin__ import * #My interpreter was shirking adding this automatically on the non-generated files. Most shouldn't need this, figure out why on a second pass

import sys
import os
import re
import traceback

from trakerr_client.models import *
from six import iteritems


class EventTraceBuilder(object):
    """
    Methods for storing and returning an error as a Stack object to send out to trakerr

    All members methods are @classmethods.
    """

    @classmethod
    def get_event_traces(self, exc_info = None):
        """
        """

        trace = Stacktrace()
        try:
            if exc_info is None: exc_info = sys.exc_info()

            self.add_stack_trace(trace, exc_info)
            return trace
        finally:
            del exc_info

    @classmethod
    def add_stack_trace(self, trace_list, exc_info=None):
        """
        """

        try:
            if exc_info is None: exc_info = sys.exc_info()
            newTrace = InnerStackTrace()

            e_type, value, tb = exc_info
            newTrace.trace_lines = self.get_event_tracelines(tb)
            newTrace.type = Trakerr_Utils.format_error_name(e_type)
            newTrace.message = str(value)
            trace_list.append(newTrace)
        finally:
            del exc_info

    @classmethod
    def get_event_tracelines(self, tb):
        """
        """

        stacklines = StackTraceLines()
        st_line = StackTraceLine()

        for filename, line, func, text in traceback.extract_tb(tb):
            st_line.file = filename
            st_line.line = line
            st_line.function = func

        stacklines.append(st_line)
        return stacklines



class Trakerr_Utils(object):

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
     


