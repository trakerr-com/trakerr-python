# coding: utf-8

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

from __future__ import absolute_import
from __builtin__ import *  #My interpreter was shirking adding this automatically on the non-generated files. Most shouldn't need this, figure out why on a second pass

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from trakerr_client import ApiClient
from trakerr_client import EventsApi
from trakerr_client.apis import events_api
from trakerr_client.models import *
from event_trace_builder import EventTraceBuilder, Trakerr_Utils
from datetime import datetime, timedelta


class Trakerr(object):
    """
    The public facing class that will log errors.

    A use case is:
    >>>from trakerr__client import Trakerr
    >>>...
    >>>l = Trakerr()
    >>>...
    >>>try:
    >>>   ...
    >>>except:
    >>>   l.log("Optional Error String")
    """

    def __init__(self): #Add args
        raise NotImplementedError
        

    def log(self, classification = "Error", error_type = None, error_message = None, exc_info = None):
        """
        
        """
        #consider a configuration file for later. Removed my personal data for pushes for now.

        
        try:
            if exc_info is None: exc_info = sys.exc_info()
            if exc_info is not False:
                type, value = exc_info[:2]
                if error_type is None: Trakerr_Utils.format_error_name(type)
                if error_message is None: str(value)
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
        """

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

    def create_new_app_event(self, classification="Error", eventType="unknown",
                             eventMessage="unknown"):  # Default None the arguments if they're not required?
        """
        """

        return AppEvent(self.api_Key, classification, eventType, eventMessage)

    def send_event(self, app_event):
        """
        """

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

        self.fill_defaults(app_event)
        self.events_api.events_post(app_event, callback=self.async_callback)



    def fill_defaults(self, app_event):
        """
        Checks the given app event, and if it each event field is not filled out in a specific case, fill out the the event with the instance defaults.
        Returns the fully filled out AppEvent object, while also filling out the instance passed in

        :param app_event:  The app event to fill parameters out.
        :return: The given AppEvent object after it is checked and filled out.
        """

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
