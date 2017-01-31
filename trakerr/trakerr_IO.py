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

from __builtin__ import *  #My interpreter was shirking adding this automatically on the non-generated files. Most shouldn't need this, figure out why on a second pass

import sys
import os
import re
import platform

# python 2 and python 3 compatibility library
from six import *

#might want to clean up imports?
from trakerr_client import ApiClient, EventsApi
from trakerr_client.apis import events_api
from trakerr_client.models import *
from event_trace_builder import EventTraceBuilder
from trakerr_utils import TrakerrUtils
from datetime import datetime, timedelta


class TrakerrIO(object):
    """
    The public facing class that will log errors.

    A standard use case without the handler is:
    >>>from trakerr__client import trakerr
    >>>...
    >>>l = trakerr("API Key", "app_version")
    >>>...
    >>>try:
    >>>   ...
    >>>except:
    >>>   l.log()
    """

    def __init__(self, api_key, app_version, url = TrakerrUtils.SERVER_URL, datacenter = None, datacenter_region = None):
        """
        """
        if (not isinstance(api_key, string_types) or not isinstance(url, string_types) or not isinstance(app_version, string_types)
                or (datacenter is not None and not isinstance(datacenter, string_types)) or (datacenter_region is not None and not isinstance(datacenter_region, string_types))):
            raise TypeError("Arguments are expected strings.")

        self.Api_Key = api_key
        self.URL = url
        self.App_Version = app_version
        self.Datacenter = datacenter
        self.Datacenter_Region = datacenter_region

    def log(self, classification = "ERROR", error_type = None, error_message = None, exc_info = None):
        """
        
        """

        #consider a configuration file for later. Removed my personal data for pushes for now.
        client = TrakerrClient(self.Api_Key, self.URL, self.App_Version, platform.python_implementation(), platform.python_version(),
                              platform.node(), platform.system() + " " + platform.release(), platform.version(), self.Datacenter, self.Datacenter_Region)
      
        try:
            if exc_info is None: exc_info = sys.exc_info()
            if exc_info is not False:
                #//TODO: Add check for exc_info here.
                type, value = exc_info[:2]
                if error_type is None: error_type = TrakerrUtils.format_error_name(type)
                if error_message is None: error_message = str(value)

            if not isinstance(classification, string_types) or not isinstance(error_type, string_types) or not isinstance(error_message, string_types):
                raise  TypeError("Arguments are expected strings.") #Do the type check before you creat a new event, hence why we can't merge the two if not false statements

            excevent = client.create_new_app_event(classification, error_type, error_message)

            if exc_info is not False:
                excevent.event_stacktrace = EventTraceBuilder.get_event_traces(exc_info)
            client.send_event_async(excevent)

        finally:
            del exc_info


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

    def __init__(self, api_key=None, url_path=None, context_app_version=None, context_env_name="development", context_env_version=None,
                 context_env_hostname=None,
                 context_appos=None, context_appos_version=None, context_datacenter=None,
                 context_datacenter_region=None):
        """

        :param context_env_name: The string name of the enviroment the code is running on.
        :param context_env_version: The string version of the enviroment the code is running on.
        """

        test8 = (context_datacenter_region is not None and isinstance(context_datacenter_region, string_types))
        if ((api_key is not None and not isinstance(api_key, string_types)) or (url_path is not None and not isinstance(url_path, string_types))
                or (context_app_version is not None and not isinstance(context_app_version, string_types)) or not isinstance(context_env_name, string_types)
                or (context_env_hostname is not None and not isinstance(context_env_hostname, string_types)) or (context_appos is not None and not isinstance(context_appos, string_types))
                or (context_appos_version is not None and not isinstance(context_appos_version, string_types)) 
                or (context_datacenter is not None and not isinstance(context_datacenter, string_types))
                or (context_datacenter_region is not None and not isinstance(context_datacenter_region, string_types))):
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
        if url_path is None:
            client = ApiClient()
        else:
            client = ApiClient(url_path)
        self.events_api = EventsApi(client)

    def create_new_app_event(self, classification="ERROR", event_type="unknown",
                             event_message="unknown"):  # Default None the arguments if they're not required?
        """
        """
        if not isinstance(classification, string_types) or not isinstance(event_type, string_types) or not isinstance(event_message, string_types):
            raise TypeError("Arguments are expected strings.")

        return AppEvent(self.api_Key, classification, event_type, event_message)

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

        #print response

    def send_event_async(self, app_event):
        """
        """

        if not isinstance(app_event, AppEvent):
            raise TypeError("Argument is expected of class AppEvent.")

        self.fill_defaults(app_event)
        self.events_api.events_post(app_event, callback=self.async_callback)



    def fill_defaults(self, app_event):
        """
        Checks the given app event, and if it each event field is not filled out in a specific case, fill out the the event with the instance defaults.
        Returns the fully filled out AppEvent object, while also filling out the instance passed in

        :param app_event:  The app event to fill parameters out.
        :return: The given AppEvent object after it is checked and filled out.
        """

        if not isinstance(app_event, AppEvent):
            raise TypeError("Argument is expected of class AppEvent.")

        if app_event.api_key is None: app_event.apiKey = self.api_Key

        if app_event.context_app_version is None: app_event.context_app_version = self.context_App_Version
        if app_event.context_env_name is None: app_event.context_env_name = self.context_Env_Name
        if app_event.context_env_version is None: app_event.context_env_version = self.context_Env_Version
        if app_event.context_env_hostname is None: app_event.context_env_hostname = self.context_Env_Hostname

        if app_event.context_app_os is None:
            app_event.context_app_os = self.context_AppOS
            app_event.context_app_os_version = self.context_AppOS_Version

        if app_event.context_data_center is None: app_event.context_data_center = self.context_DataCenter
        if app_event.context_data_center_region is None: app_event.context_data_center_region = self.context_DataCenter_Region

        TD = datetime.utcnow() - self.EPOCH_CONSTANT #timedelta object
        if app_event.event_time is None: app_event.event_time = int(TD.total_seconds()*1000)
        return app_event #Since we're filling out an an instance, probably don't need this.