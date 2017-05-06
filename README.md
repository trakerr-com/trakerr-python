# Trakerr - Python API client
Get your application events and errors to Trakerr via the *Trakerr API*.

You will need your API key to send events to trakerr.

## Requirements
Python 2.7 and 3.4+

## 3-minute Integration Guide
If you're already using the python logger in some capacity, you can integrate with Trakerr quickly. First, issue a pip install to get the latest version:

To install from master, simply use:
```bash
pip install git+https://github.com/trakerr-io/trakerr-python.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/trakerr-io/trakerr-python.git`)

Once installation is complete, add this import from wherever you instantiate your loggers.

```python
import logging #Your previous logging import here
from trakerr import TrakerrHandler #New import.
```

And then you'll need to create a handler and a logger object and attach them before you can use them later on.

```python
#Your original logger.
logger = logging.getLogger("Logger name")
#Instantiate Trakerr's logger handler. By default the handler will only log WARNING and above.
th = TrakerrHandler("<api-key>", "App Version number here", "Deployment stage here")
#Attach our handler to your logger.
logger.addHandler(th)
```
The handler's full constructor signature is as follows:
```python
def __init__(self, api_key=None, app_version="1.0", context_deployment_stage="deployment",
                 client=None, level=logging.WARNING):
```
The parameters are as follows
- **api_key**: should be your api key from trakerr.
- **app_version**: should be your code's app version.
- **deployment_stage**: is the stage of the codebase you are pulling events from (production, test, development, ect). 
- **client**: allows you to pass in a preconfigured `TrakerrClient` instance, which allows you to provide a client with custom values. If you provide a client, the values of the first three parameters do not matter.
- **level**: Allows you to set the level of events that this handler can emit. By default, TrakerrHandler will send warnings and above to trakerr. This way, if you're using more than one handler, you can set the logger to log all events, and set trakerr to log only warnings and above, while sending infos and above with another handler.

You should be able to now send basic events and information to trakerr. If you are only using trakerr to log, or want to send more in depth events, read on below.

## Detailed Integration Guide
By using the pip command above, you can also use trakerr in a multitude of different ways.

### Option-1: Attaching Trakerr to an exsisting logger
Follow the instructions in the [three minute integration guide](#3-minute-Integration-Guide) to attach trakerr to a logger you've already written.

### Option-2: Creating a new logger for Trakerr
Along with your imports, add:

```python
from trakerr import Trakerr
```

And then you can get a python logger object that ties in to trakerr to handle the various levels of errors, giving the appropriate data as strings.

```python
def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    logger = Trakerr.getLogger("<api-key>", "App Version number here", "Logger Name")

    try:
        raise FloatingPointError()
    except:
       logger.exception("Bad math.")

    return 0
```

### Option-3: Sending an error(or non-error) quickly without using the logger
You can quickly send a simple event with partial custom data from the log function of the `TrakerrClient`. Add these imports:

```python
from trakerr import TrakerrClient
```

you can then send call log simply to send a quick error to Trakerr. Note the values that the argument dictionary takes are in the log docstring.

```python
client = TrakerrClient("<api-key>", "App Version number")

client.log({"user":"jill@trakerr.io", "session":"25", "errname":"user logon issue",
            "errmessage":"User refreshed the page."}, "info", "logon script", False)
```

You can call this from an `except` and leave off the false parameter if you wish to send an error with a stacktrace.

### Option-4: Add Custom Data
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

    client = TrakerrClient("<api-key>", "App Version number")

    try:
        raise IndexError("Bad Math")
    except:
        appevent = client.create_new_app_event_error("ERROR", "Index Error", "Math")
        
        #You can use this call to create an app event
        #appevent = client.create_new_app_event("ERROR", "Index Error", "Math")
        #without a stacktrace, in case you do don't have a stacktrace or you're not sending a crash.

        #Populate any field with your own data, or send your own custom data
        appevent.context_app_browser = "Chrome"
        appevent.context_app_browser_version = "57.0.2987.133"
        appevent.custom_properties = CustomData()
        
        #Can support multiple string data
        appevent.custom_properties.string_data = CustomStringData("Custom String Data 1", "Custom String Data 2")
        appevent.custom_properties.string_data.custom_data3 = "More Custom Data!"
        
        #populate the user and session to the error event
        appevent.event_user = "john@traker.io"
        appevent.event_session = "6"

        #send it to trakerr
        client.send_event_async(appevent)

    return 0
```

If you are using Django, we recommend that you look at [django user agents](https://github.com/selwin/django-user_agents) as a simple and quick way of getting the browser's name and version rather than parsing the user agent yourself. The library also allows you to use the client browser in the template, allowing you to modify the front end to the error accordingly. Please note that this library is _not maintained by Trakerr_.

## An in-depth look at TrakerrClient's properties
TrakerrClient's constructor initalizes the default values to all of TrakerrClient's properties.

```python
def __init__(self, api_key, context_app_version = "1.0", context_deployment_stage =  "development"):
```

The TrakerrClient class however has a lot of exposed properties. The benefit to setting these immediately after after you create the TrakerrClient is that AppEvent will default it's values against the `TrakerrClient` instance that created it. This way if there is a value that all your AppEvents uses, and the constructor default value currently doesn't suit you; it may be easier to change it in the `TrakerrClient` instance as it will become the default value for all AppEvents created after. A lot of these are populated by default value by the constructor, but you can populate them with whatever string data you want. The following table provides an in depth look at each of those.


Name | Type | Description | Notes
------------ | ------------- | -------------  | -------------
**apiKey** | **string** | API key generated for the application | 
**contextAppVersion** | **string** | Application version information. | Default value: `1.0`
**contextDevelopmentStage** | **string** | One of development, staging, production; or a custom string. | Default Value: `development`
**contextEnvLanguage** | **string** | Constant string representing the language the application is in. | Default value: `python`
**contextEnvName** | **string** | Name of the interpreter the program is run on. | Default Value: `platform.python_implementation()`
**contextEnvVersion** | **string** | Version of python this program is running on. | Default Value: `platform.python_version()`
**contextEnvHostname** | **string** | Hostname or ID of environment. | Default value: `platform.node()`
**contextAppOS** | **string** | OS the application is running on. | Default value: `platform.system() + platform.release()`
**contextAppOSVersion** | **string** | OS Version the application is running on. | Default value: `platform.version()`
**contextAppOSBrowser** | **string** | An optional string browser name the application is running on. | Defaults to `None`
**contextAppOSBrowserVersion** | **string** | An optional string browser version the application is running on. | Defaults to `None`
**contextDataCenter** | **string** | Data center the application is running on or connected to. | Defaults to `None`
**contextDataCenterRegion** | **string** | Data center region. | Defaults to `None`

## Advanced pip install commands for Trakerr
You can run the following command to update an exsisting installation to the latest commit on master:
```bash
pip install git+https://github.com/trakerr-io/trakerr-python.git --upgrade
```

You can install from a branch (Not recommended for production use):
```bash
pip install git+https://github.com/trakerr-io/trakerr-python.git#<branch_name_here>
```

## Documentation For Models

 - [AppEvent](https://github.com/trakerr-io/trakerr-python/blob/master/generated/docs/AppEvent.md)

## Author
[RM](https://github.com/RMSD)
