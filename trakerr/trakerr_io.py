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
    ------------------------------------------------------------------------------
    psutils is licensed under the BSD 2-0. For more information please see their licencing information:
    https://github.com/giampaolo/psutil/blob/master/LICENSE.
"""

import platform
import pprint
import sys
import re

import psutil
from datetime import datetime
from six import *

# might want to clean up imports?
from trakerr_client import ApiClient, Configuration
from trakerr_client.apis import EventsApi
from trakerr_client.models import AppEvent

from trakerr.event_trace_builder import EventTraceBuilder
from trakerr.trakerr_utils import TrakerrUtils
from trakerr.perf_utils import PerfUtils


class TrakerrClient(object):
    """
    An object which controls creating and sending AppEvents.
    """

    _comp_info = PerfUtils.instance()

    # instance variables and properties
    # event_api

    # api_key
    # context_app_version
    # context_env_name
    # context_env_version
    # context_env_hostname
    # context_appos
    # context_appos_version
    # context_appbrowser
    # context_appbrowser_version
    # context_datacenter
    # context_datacenter_region
    # context_application_sku
    # context_tags

    EPOCH_CONSTANT = datetime(1970, 1, 1)

    def __init__(self, api_key, context_app_version="1.0",
                 context_deployment_stage="development", application_sku="", tags=[],
                 threads=4, connnections=4):
        """
        Initializes the TrakerrClient class and default values for it's properties.
        :param api_key: The API key for your application on trakerr to send events back to.
        :param context_env_name: The string name of the enviroment the code is running on.
        :param context_deployment_stage: The string version of the enviroment
         the code is running on.
        :param application_sku: Optional string application SKU.
        :param tags: Optional list of string tags on the module
         or part of project you are logging events on.
         It is recommended at least giving giving the module and the submodule as tags.
         IE: ["mysql", "payment"]
        :param threads: Number of threads in the thread pool.
         This only matters if you are using async call in python 3.2+.
        :param connection: Number of connections in the connection pool.
         If there are more threads than connections,
         the connection pool will block those calls until it can serve a connection.
        """

        if (not isinstance(api_key, string_types)
                or not isinstance(context_app_version, string_types)
                or not isinstance(context_deployment_stage, string_types)
                or not isinstance(application_sku, string_types)):
            raise TypeError("Arguments are expected strings")

        # pep8 linters wants you to init the private variable (which is good practice in python)
        # before the public property getters and setters. Hence the
        # preappending self._(privatevariable).
        seq = " "
        self._api_key = self.api_key = api_key
        self._context_app_version = self.context_app_version = context_app_version
        self._context_deployment_stage = self.context_deployment_stage = context_deployment_stage
        self._context_application_sku = self.context_application_sku = application_sku
        self._context_env_language = self.context_env_language = "Python"
        self._context_env_name = self.context_env_name = platform.python_implementation()
        self._context_env_version = self.context_env_version = platform.python_version()
        self._context_env_hostname = self.context_env_hostname = platform.node()


        if re.search('windows', platform.system().lower()) is not None:
            # Join is supposed to be faster than + operator
            self._context_appos = self.context_appos = seq.join(
                (platform.system(), platform.release()))
            self._context_appos_version = self.context_appos_version = platform.version()
        else:
            self._context_appos = self.context_appos = platform.system()
            self._context_appos_version = self.context_appos_version = platform.release()

        self._context_appbrowser = self.context_appbrowser = None
        self._context_appbrowser_version = self.context_appbrowser_version = None
        self._context_datacenter = self.context_datacenter = None
        self._context_datacenter_region = self.context_datacenter_region = None

        self._events_api = EventsApi(ApiClient(Configuration().host, threads=threads, connnections=connnections))
        # Should get the default url. Also try Configuration().host
        self._comp_info = PerfUtils.instance()

        #psutil.cpu_percent()

        try:
            self._context_tags = self.context_tags = list(tags)
        except TypeError:
            pprint.pprint("tags are unable to be processed into a list object. \
                           Please us a list or a list like structure.", sys.stderr)

    def create_new_app_event(self, log_level="error", classification="issue", event_type="unknown",
                             event_message="unknown", exc_info=False):
        """
        Creates a new AppEvent instance.
        :param log_level: Strng representation on the level of the error.
        Can be 'debug','info','warning','error', 'fatal', defaults to 'error'.
        :param classification: Optional extra string descriptor to clarify the error.
        :param event_type: String representation of the type of error.
        :param event_message: String message of the error.
        :param exc_info: The exc_info tuple to parse the stacktrace from.
        Pass None to generate one from the current error stack;
        pass false to skip parsing the stacktrace.
        :return: AppEvent instance with exc_info parsed depending on the above flags.
        """
        try:
            if exc_info is True or exc_info is None:
                exc_info = sys.exc_info()
                if not any(exc_info):
                    exc_info = False

            if exc_info is not False:
                if not TrakerrUtils.is_exc_info_tuple(exc_info):
                    raise TypeError(
                        "exc_info is expected an exc_info info tuple or False.")
                errtype, value = exc_info[:2]
                if event_type is None or event_type == "unknown":
                    event_type = TrakerrUtils.format_error_name(errtype)
                if event_message is None or event_message == "unknown":
                    event_message = str(value)

            if (not isinstance(log_level, string_types)
                    or (not isinstance(classification, string_types)
                        and classification is not None)
                    or (not isinstance(event_type, string_types)
                        and event_type is not None)
                    or (not isinstance(event_message, string_types)
                        and event_message is not None)):
                # Do the type check before you creat a new event, hence why we
                # can't merge the two if not false statements.
                raise TypeError("Arguments are expected strings or None.")

            #Accepted value string parsing.
            #Leave the appevent incase someone wants to fill it out themselves as an error.
            #But we just want to default to error here.
            excevent = AppEvent(self.api_key, classification=classification,
                                event_type=event_type, event_message=event_message)

            #Of all things, the python logger logs fatals as criticals.
            #I'll correct it manually here.
            if log_level == "critical":
                log_level = "fatal"
            try:
                excevent.log_level = log_level.lower()
            except ValueError:
                excevent.log_level = "error"

            if exc_info is not False:
                excevent.event_stacktrace = EventTraceBuilder.get_event_traces(
                    exc_info)
        finally:
            del exc_info

        return excevent

    def send_event(self, app_event):
        """
        Sends the given AppEvent instance to trakerr.
        :param app_event: AppEvent instance to send to trakerr.
        """
        if not isinstance(app_event, AppEvent):
            raise TypeError("Argument is expected of class AppEvent.")

        self.fill_defaults(app_event)
        data, response = self._events_api.events_post_with_http_info(app_event)[:2]
        return (data, response)

    def send_event_async(self, app_event, call_back=None):
        """
        Asyncronously sends the given AppEvent instance to trakerr.
        :param app_event: AppEvent instance to send to trakerr.
        :param call_back: Callback method for the async call.
        defaults to module level async_callback.
        """

        if not isinstance(app_event, AppEvent):
            raise TypeError("Argument is expected of class AppEvent.")

        if call_back is None:
            call_back = async_callback

        self.fill_defaults(app_event)
        self._events_api.events_post_with_http_info(app_event, callback=call_back)

    def log(self, arg_dict, log_level="error", classification="issue", exc_info=True):
        """
        Creates an AppEvent and sends it with the default values to all fields.
        Allows the caller to pass in user and session as added information to log,
        to file the error under.
        :param arg_dict: Dictionary with any of these key value pairs assigned to a string:
        eventtype, eventmessage, user, session, time for operation time in milis,
        url if it is a web app, corrid for the correlation id,
        and device for the machine name (samsung s7).
        You can leave any pair out that you don't need.
        To construct with pure default values, pass in an empty dictionary.
        If you are passing an event with a Stacktrace errname
        and message will be filled with the values from Stacktrace.
        Otherwise, both errname and errmessage will be unknown.
        :param log_level: String representation on the level of the error.
        Can be 'debug', 'info', 'warning', 'error', 'fatal', defaults to 'error'.
        :param classification: Optional extra string descriptor to clarify the error.
        (IE: log_level is fatal and classification may be 'hard lock' or 'Network error')
        :param exc_info: exc_info tuple to parse.
        Default None to generate a exc_info tuple from the current stacktrace.
        Pass False to not generate an exc_info tuple.
        """
        excevent = self.create_new_app_event(log_level,
                                             classification, arg_dict.get(
                                                 'eventtype'),
                                             arg_dict.get('eventmessage'), exc_info)
        excevent.event_user = arg_dict.get('user')
        excevent.event_session = arg_dict.get('session')
        excevent.context_operation_time_millis = arg_dict.get('time')
        excevent.context_url = arg_dict.get('url')
        excevent.context_cross_app_correlation_id = arg_dict.get('corrid')
        excevent.context_device = arg_dict.get('device')
        self.send_event_async(excevent)

    def fill_defaults(self, app_event):
        """
        Checks the given app event, and if it each event field is not filled out in a specific case,
        fill out the the event with the instance defaults.
        :param app_event:  The app event to fill parameters out.
        :return: The fully filled out AppEvent object,
        while also filling out the instance passed in.
        """

        if not isinstance(app_event, AppEvent):
            raise TypeError("Argument is expected of class AppEvent.")

        if app_event.api_key is None:
            app_event.api_key = self.api_key

        if app_event.context_app_version is None:
            app_event.context_app_version = self.context_app_version
        if app_event.deployment_stage is None:
            app_event.deployment_stage = self.context_deployment_stage

        if app_event.context_env_language is None:
            app_event.context_env_language = self.context_env_language
        if app_event.context_env_name is None:
            app_event.context_env_name = self.context_env_name
        if app_event.context_env_version is None:
            app_event.context_env_version = self.context_env_version
        if app_event.context_env_hostname is None:
            app_event.context_env_hostname = self.context_env_hostname

        if app_event.context_app_os is None:
            app_event.context_app_os = self.context_appos
        if app_event.context_app_os_version is None:
            app_event.context_app_os_version = self.context_appos_version

        if app_event.context_app_browser is None:
            app_event.context_app_browser = self.context_appbrowser
        if app_event.context_app_browser_version is None:
            app_event.context_app_browser_version = self.context_appbrowser_version

        if app_event.context_data_center is None:
            app_event.context_data_center = self.context_datacenter
        if app_event.context_data_center_region is None:
            app_event.context_data_center_region = self.context_datacenter_region

        tdo = datetime.utcnow() - self.EPOCH_CONSTANT  #timedelta object
        if app_event.event_time is None:
            app_event.event_time = int(tdo.total_seconds() * 1000)

        if app_event.context_cpu_percentage is None:
            app_event.context_cpu_percentage = self._comp_info.get_cpu_percent()
        if app_event.context_memory_percentage is None:
            app_event.context_memory_percentage = self._comp_info.get_mem_percent()

        if app_event.context_tags is None:
            app_event.context_tags = self.context_tags

        if app_event.context_app_sku is None:
            app_event.context_app_sku = self.context_app_version

    @classmethod
    def shutdown(cls):
        TrakerrClient._comp_info.shutdown()


    #getters and setters
    @property
    def api_key(self):
        """api_key property"""
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    @api_key.deleter
    def api_key(self):
        del self._api_key

    @property
    def context_app_version(self):
        """context_app_version property"""
        return self._context_app_version

    @context_app_version.setter
    def context_app_version(self, value):
        self._context_app_version = value

    @context_app_version.deleter
    def context_app_version(self):
        del self._context_app_version

    @property
    def context_env_name(self):
        """context_env_name property"""
        return self._context_env_name

    @context_env_name.setter
    def context_env_name(self, value):
        self._context_env_name = value

    @context_env_name.deleter
    def context_env_name(self):
        del self._context_env_name

    @property
    def context_env_version(self):
        """context_env_version property"""
        return self._context_env_version

    @context_env_version.setter
    def context_env_version(self, value):
        self._context_env_version = value

    @context_env_version.deleter
    def context_env_version(self):
        del self._context_env_hostname

    @property
    def context_env_hostname(self):
        """context_env_hostname property"""
        return self._context_env_hostname

    @context_env_hostname.setter
    def context_env_hostname(self, value):
        self._context_env_hostname = value

    @context_env_hostname.deleter
    def context_env_hostname(self):
        del self._context_env_hostname

    @property
    def context_appos(self):
        """context_appos property"""
        return self._context_appos

    @context_appos.setter
    def context_appos(self, value):
        self._context_appos = value

    @context_appos.deleter
    def context_appos(self):
        del self._context_appos

    @property
    def context_appos_version(self):
        """context_appos_version property"""
        return self._context_appos_version

    @context_appos_version.setter
    def context_appos_version(self, value):
        self._context_appos_version = value

    @context_appos_version.deleter
    def context_appos_version(self):
        del self._context_appos_version

    @property
    def context_appbrowser(self):
        """context_app_browser property"""
        return self._context_appbrowser

    @context_appbrowser.setter
    def context_appbrowser(self, value):
        self._context_appbrowser = value

    @context_appbrowser.deleter
    def context_appbrowser(self):
        del self._context_appbrowser

    @property
    def context_appbrowser_version(self):
        """context_app_browser_version property"""
        return self._context_appbrowser_version

    @context_appbrowser_version.setter
    def context_appbrowser_version(self, value):
        self._context_appbrowser_version = value

    @context_appbrowser_version.deleter
    def context_appbrowser_version(self):
        del self._context_appbrowser_version

    @property
    def context_datacenter(self):
        """context_datacenter property"""
        return self._context_datacenter

    @context_datacenter.setter
    def context_datacenter(self, value):
        self._context_datacenter = value

    @context_datacenter.deleter
    def context_datacenter(self):
        del self._context_datacenter

    @property
    def context_datacenter_region(self):
        """context_data_center_region property"""
        return self._context_datacenter_region

    @context_datacenter_region.setter
    def context_datacenter_region(self, value):
        self._context_datacenter_region = value

    @context_datacenter_region.deleter
    def context_datacenter_region(self):
        del self._context_datacenter_region

    @property
    def context_deployment_stage(self):
        """context_deployment_stage property"""
        return self._context_deployment_stage

    @context_deployment_stage.setter
    def context_deployment_stage(self, value):
        self._context_deployment_stage = value

    @context_deployment_stage.deleter
    def context_deployment_stage(self):
        del self._context_deployment_stage

    @property
    def context_env_language(self):
        """context_env_language property"""
        return self._context_env_language

    @context_env_language.setter
    def context_env_language(self, value):
        self._context_env_language = value

    @context_env_language.deleter
    def context_env_language(self):
        del self._context_env_language

    @property
    def context_tags(self):
        """context_tags property"""
        return self._context_tags

    @context_tags.setter
    def context_tags(self, value):
        self._context_tags = value

    @context_tags.deleter
    def context_tags(self):
        del self._context_tags



def async_callback(response):
    """
    Callback method for the send_event_async function. Currently outputs nothing.
    :param response: message returned after the async call is completed.
    """

    #pprint.pprint(str(response), sys.stderr)
