# coding: utf-8

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

import platform
import sys
from datetime import datetime

from six import *

from event_trace_builder import EventTraceBuilder
# might want to clean up imports?
from trakerr_client import ApiClient, EventsApi
from trakerr_client.apis import events_api
from trakerr_client.models import *
from trakerr_utils import TrakerrUtils


class TrakerrClient(object):
    """
    Description of class
    """

    # Implied class variable
    # event_Api

    # api_Key
    # context_App_Version
    # context_Env_Name
    # context_Env_Version
    # context_Env_Hostname
    # context_AppOS
    # context_AppOS_Version
    # context_DataCenter
    # context_DataCenter_Region

    EPOCH_CONSTANT = datetime(1970, 1, 1)

    def __init__(self, api_key, context_app_version=None, context_env_name="development",
                 context_env_version=platform.python_implementation()
                 + " " + platform.python_version(),

                 context_env_hostname=platform.node(),
                 context_appos=platform.system() + " " + platform.release(),
                 context_appos_version=platform.version(),
                 context_datacenter=None, context_datacenter_region=None,
                 url_path=TrakerrUtils.SERVER_URL,):
        """

        :param context_env_name: The string name of the enviroment the code is running on.
        :param context_env_version: The string version of the enviroment the code is running on.
        """

        if (not isinstance(api_key, string_types) or not isinstance(url_path, string_types)
                or (not isinstance(context_app_version, string_types)
                    and context_app_version is not None)
                or (not isinstance(context_env_name, string_types)
                    and context_env_name is not None)
                or (not isinstance(context_env_hostname, string_types)
                    and context_env_hostname is not None)
                or (not isinstance(context_appos, string_types)
                    and context_appos is not None)
                or (not isinstance(context_appos_version, string_types)
                    and context_appos is not None)
                or (not isinstance(context_datacenter, string_types)
                    and context_datacenter is not None)
                or (not isinstance(context_datacenter_region, string_types)
                    and context_datacenter_region is not None)):
            raise TypeError("Arguments are expected strings")

        self.api_Key = api_key

        self.context_App_Version = context_app_version
        self.context_Env_Name = context_env_name
        self.context_Env_Version = context_env_version
        self.context_Env_Hostname = context_env_hostname
        self.context_AppOS = context_appos
        self.context_AppOS_Version = context_appos_version
        self.context_DataCenter = context_datacenter
        self.context_DataCenter_Region = context_datacenter_region

        self.events_api = EventsApi(ApiClient(url_path))

    # Default None the arguments if they're not required?
    def create_new_app_event(self, classification="ERROR", event_type=None, event_message=None):
        """
        """
        if (not isinstance(classification, string_types)
                or not isinstance(event_type, string_types)
                or not isinstance(event_message, string_types)):
            raise TypeError("Arguments are expected strings.")

        return AppEvent(self.api_Key, classification, event_type, event_message)

    def create_new_app_event_error(self, classification="ERROR", event_type=None,
                                   event_message=None, exc_info=None):
        """
        """
        try:
            if exc_info is None:
                exc_info = sys.exc_info()
            if exc_info is not False:
                #//TODO: Add check for exc_info here.
                type, value = exc_info[:2]
            if event_type is None:
                # Error if exec_into is None/False and error type is none?
                event_type = TrakerrUtils.format_error_name(type)
            if event_message is None:
                event_message = str(value)

            if not isinstance(classification, string_types) or not isinstance(event_type, string_types) or not isinstance(event_message, string_types):
                # Do the type check before you creat a new event, hence why we
                # can't merge the two if not false statements.
                raise TypeError("Arguments are expected strings.")

            excevent = self.create_new_app_event(
                classification, event_type, event_message)
            excevent.event_stacktrace = EventTraceBuilder.get_event_traces(
                exc_info)

        finally:
            del exc_info

        return excevent

    def send_event(self, app_event):
        """
        """
        if not isinstance(app_event, AppEvent):
            raise TypeError("Argument is expected of class AppEvent.")

        self.fill_defaults(app_event)
        self.events_api.events_post(app_event)

    def async_callback(self, response):
        """
        Callback method for the send_event_async function. Currently outputs nothing.

        :param response: message returned after the async call is completed.
        """

        # print response

    def send_event_async(self, app_event):
        """
        """

        if not isinstance(app_event, AppEvent):
            raise TypeError("Argument is expected of class AppEvent.")

        self.fill_defaults(app_event)
        self.events_api.events_post(app_event, callback=self.async_callback)

    def log(self, classification="ERROR", error_type=None, error_message=None, exc_info=None):
        """
        """

        excevent = self.create_new_app_event_error(
            classification, error_type, error_message, exc_info)
        self.send_event_async(excevent)

    def fill_defaults(self, app_event):
        """
        Checks the given app event, and if it each event field is not filled out in a specific case, fill out the the event with the instance defaults.
        Returns the fully filled out AppEvent object, while also filling out the instance passed in

        :param app_event:  The app event to fill parameters out.
        """

        if not isinstance(app_event, AppEvent):
            raise TypeError("Argument is expected of class AppEvent.")

        if app_event.api_key is None:
            app_event.apiKey = self.api_Key

        if app_event.context_app_version is None:
            app_event.context_app_version = self.context_App_Version
        if app_event.context_env_name is None:
            app_event.context_env_name = self.context_Env_Name
        if app_event.context_env_version is None:
            app_event.context_env_version = self.context_Env_Version
        if app_event.context_env_hostname is None:
            app_event.context_env_hostname = self.context_Env_Hostname

        if app_event.context_app_os is None:
            app_event.context_app_os = self.context_AppOS
            app_event.context_app_os_version = self.context_AppOS_Version

        if app_event.context_data_center is None:
            app_event.context_data_center = self.context_DataCenter
        if app_event.context_data_center_region is None:
            app_event.context_data_center_region = self.context_DataCenter_Region

        TD = datetime.utcnow() - self.EPOCH_CONSTANT  # timedelta object
        if app_event.event_time is None:
            app_event.event_time = int(TD.total_seconds() * 1000)
