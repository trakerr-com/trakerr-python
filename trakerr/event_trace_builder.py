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

import sys
import traceback

from six import *

from trakerr_client.models import *
from trakerr_utils import TrakerrUtils


class EventTraceBuilder(object):
    """
    Methods for storing and returning an error as a Stack object to send out to trakerr

    All members methods are @classmethods.
    """

    @classmethod
    def get_event_traces(cls, exc_info=None):
        """
        """

        trace = Stacktrace()
        try:
            if exc_info is None: exc_info = sys.exc_info()

            #TODO: Add check for exc_info
            cls.add_stack_trace(trace, exc_info)
            return trace
        finally:
            del exc_info

    @classmethod
    def add_stack_trace(cls, trace_list, exc_info=None):
        """
        """

        try:
            if exc_info is None:
                exc_info = sys.exc_info()

            if not isinstance(trace_list, Stacktrace):#TODO: Add check for exc_info
                raise TypeError("An argument is not the correct type.")
            newtrace = InnerStackTrace()

            e_type, value, tb_ = exc_info
            newtrace.trace_lines = cls.get_event_tracelines(tb_)
            newtrace.type = TrakerrUtils.format_error_name(e_type)
            newtrace.message = str(value)
            trace_list.append(newtrace)
        finally:
            del exc_info

    @classmethod
    def get_event_tracelines(cls, tb_):
        """
        """

        stacklines = StackTraceLines()

        for filename, line, func, _ in traceback.extract_tb(tb_):
            st_line = StackTraceLine()
            st_line.file = filename
            st_line.line = line
            st_line.function = func
            stacklines.append(st_line)

        return stacklines
