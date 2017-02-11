# trakerr_client
Get your application events and errors to Trakerr via the *Trakerr API*.

You will need your API key to send events to trakerr.

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

```sh
pip install git+https://github.com/trakerr-io/trakerr-python.git
```
(you may need to run `pip` with root permission: `pip install git+https://github.com/trakerr-io/trakerr-python.git`)

Then import the package:
```python
import trakerr
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and you're set to add Trakerr to your project. All of these examples are included in testmain.py.

### Option 1: Automatic initialization
Along with your imports, add:

```python
from trakerr import Trakerr
```

And then you can get a python logger object that ties in to trakerr to handle the various levels of errors, giving the appropriate data as strings.

```python
def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    logger = Trakerr.getLogger("API KEY", "App Version number here", "Logger Name")

    try:
        raise FloatingPointError()
    except:
       logger.exception("Bad math.")

    return 0
```

### Option 2: Manual initialization of the handler
You can initialize the handler directly and attach it to your own logger, if you want direct control over it. This is useful if you want your own custom logger. An example with the base logger follows.

You'll need to add these imports:

```python
import logging
from trakerr import TrakerrHandler
```

And then you'll need to create a handler and a logger object and attach them before you can use them later on.

```python
def main(argv=None):
    logger = logging.getLogger("Logger name")
    th = TrakerrHandler("API KEY", "App Version number here")
    logger.addHandler(th)

    try:
        raise ArithmeticError()
    except:
       logger.exception("Bad math.")

    return 0
```

### Option 3: Add Custom Data
You can send custom data as part of your error event if you need to. This circumvents the python handler. Add these imports:

```python
from trakerr import TrakerrClient
from trakerr_client.models import CustomData, CustomStringData
```

You'll then need to initialize custom properties once you create the event. Note that you can use the second call commented out to instead create an app event without a stacktrace.

```Python
def main(argv=None):
    if argv is None:
        argv = sys.argv

    client = TrakerrClient("API Key here", "App Version number")

    try:
        raise IndexError("Bad Math")
    except:
        appevent = client.create_new_app_event_error("ERROR", "Index Error", "Math")
        #appevent = client.create_new_app_event("ERROR", "Index Error", "Math") #You can use this call to create an app event
        #without a stacktrace, in case you do don't have a stacktrace or you're not sending a crash.

        #Populate any field with your own data, or send your own custom data
        appevent.context_app_os = "Windows 8"
        appevent.custom_properties = CustomData("Custom Data holder!")
        appevent.custom_properties.string_data = CustomStringData("Custom String Data 1", "Custom String Data 2") #Can support multiple string data
        appevent.custom_properties.string_data.custom_data3 = "More Custom Data!"

        #send it to trakerr
        client.send_event_async(appevent)

    return 0
```
## An in-depth look at initalizing Trakerr
Most of the examples above involve are initialized simply, since the error is populated with default values. If we take a look at the constructor, we see that there is actually plenty of fields we can fill in ourselves if we don't find the default value useful. Let's take a look at the `getlogger` Method, and the `TrakerrHandler` `__init__` since that's what `getLogger` fills in:

```python
 def getLogger(self, api_key,  app_version, name, context_env_name = platform.python_implementation(), 
               context_env_version = platform.python_version(), context_env_hostname = platform.node(),
               context_appos = platform.system() + " " + platform.release(),
               context_appos_version = platform.version(), datacenter = None, datacenter_region = None,
               client = None, url = TrakerrUtils.SERVER_URL,  level = logging.ERROR):
```

Most of the call will be explained later since most of the arguments are passed down, but the `name` field is unique to `getLogger`. Name is simply the name `TrakerrHandler` object it stores internally for identification. It is required and should be unique, but Trakerr itself does not suggest a convention on naming `Handler` objects.

The constructor for `TrakerrHandler` takes the rest of the arguments itself. The handler object acts as an intermediary between the error and Trakerr's send layers; providing the error data from the handler on emit with external facing tools. Constructor wise, it will in turn pass most it's argument to the `TrakerrClient` class, to populate the send event with the data we passed the handler to hold onto. We exposed the arguments early so as to not have to dig through the initalized `TrakerrClient` later to change them. Here's TrakerrHandler's init function.

```python
def __init__(self, api_key,  app_version, context_env_name = None, 
             context_env_version = None, context_env_hostname = None,
             context_appos = None, context_appos_version = None,
             datacenter = None, datacenter_region = None,
             client = None, url = TrakerrUtils.SERVER_URL,  level = logging.ERROR):
```

`client` lets an already initialized `TrakerrClient` object be passed in if you needed to initialize it seperately. Unless you have a need for it, leaving it none will simply create a new one instead, which should suit most cases.

`level` is something python's handler uses internally to decide when it should capture a record of a stack trace. For more information on that take a look at Python's [logging](https://docs.python.org/2/library/logging.html#logging-levels) library. The default setting is that it will emit a record on a stacktrace or above.

```python
def __init__(self, api_key, context_app_version, context_env_name = platform.python_implementation(), 
             context_env_version = platform.python_version(), context_env_hostname = platform.node(),
             context_appos = platform.system() + " " + platform.release(), 
             context_appos_version = platform.version(),
             context_datacenter = None, context_datacenter_region = None, url_path = TrakerrUtils.SERVER_URL,):
```

Finally we have the `TrakerrClient` init above. All of the data in this constructor will be sent to the server as string data (other than the `url_path` which has the url for the rest page). Refer to the reference table below for details.


Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_key** | **str** | API key generated to identfy the application | 
**context_app_version** | **str** | (optional) application version information | [optional if passed `None`] 
**context_env_name** | **str** | (optional) one of &#39;development&#39;,&#39;staging&#39;,&#39;production&#39; or a custom string | [optional if passed `None`] Default Value: "develoment"
**context_env_version** | **str** | (optional) version of environment | [optional if passed `None`] Default Value: Interpreter type(ie. cpython, ironpy) and python version (ie. 2.7.8)
**context_env_hostname** | **str** | (optional) hostname or ID of environment | [optional if passed `None`] Default value: Name of the node the program is currently run on.
**context_app_os** | **str** | (optional) OS the application is running on | [optional if passed `None`] Default value: OS name (ie. Windows, MacOS) + Release (ie. 7, 8, 10, X)
**context_app_os_version** | **str** | (optional) OS version the application is running on | [optional if passed `None`] Default value: OS provided version number
**context_data_center** | **str** | (optional) Data center the application is running on or connected to | [optional if passed `None`] 
**context_data_center_region** | **str** | (optional) Data center region | [optional if passed `None`]
**context_app_browser** | **str** | (optional) browser name if running in a browser (eg. Chrome) | [optional] For web frameworks(To be exposed and implemented)
**context_app_browser_version** | **str** | (optional) browser version if running in a browser | [optional] For web frameworks (To be exposed and implemented)
**url_path** | **str** | message containing details of the event or error | 


The server accepts the final two arguments before url_path, but they are currently in development on this api level, so if you are using django or another web framework; please use the REST API. They are not currently available in the `TrakerrClient` constructor.


## Documentation For Models

 - [AppEvent](https://github.com/trakerr-io/trakerr-python/blob/master/generated/docs/AppEvent.md)

## Author
[RM](https://github.com/RMSD)


