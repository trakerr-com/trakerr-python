# Trakerr - Python API client
Get your application events and errors to Trakerr via the *Trakerr API*.

You will need your API key to send events to trakerr.

## Requirements
Python 2.7.9+ and 3.4+

## 3-minute Integration Guide
If you're already using the python logger in some capacity, you can integrate with Trakerr quickly. First, issue a pip install to get the latest version:

To install from master, simply use:
```bash
pip install git+https://github.com/trakerr-com/trakerr-python.git
```
(you may need to run `pip` with root permission: `sudo -H pip install git+https://github.com/trakerr-com/trakerr-python.git`)

or upgrade an installation with a command from the [advanced pip commands](#Advanced-pip-install-commands-for-Trakerr) section.

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

#Attach our handler to the root logger.
logging.getLogger('').addHandler(th)

#Alternatively attach our handler to your logger for a single logger instance.
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

## TrakerrClient Shutdown
When cleaning up your application, or implementing a shutdown, be sure to call:
```python
TrakerrClient.shutdown()
```

This will close the perfomange monitoring thread gracefully. You only need to call this once, no matter how many loggers you have. Add it to any cleanup function you have for your program.

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
    
    logger = Trakerr.get_logger("<api-key>", "App Version number here", "Logger Name")

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

you can then send call log simply to send a quick error to Trakerr.

```python
client = TrakerrClient("<api-key>", "App Version number")

client.log({"user":"jill@trakerr.io", "session":"25", "eventtype":"user logon issue",
            "eventmessage":"User refreshed the page."}, "info", "logon script", False)
```

The full signature of log is as follows:
```python
def log(self, arg_dict, log_level="error", classification="issue", exc_info=True):
```

If exc\_info is True, it will poll `sys.exc_info()` for the latest error stack information. If this is false, then the event will not generate a stack trace. If exc\_info is is a tuple of exc\_info, then the event will be created using that exc\_info.

arg\_dict is a dictionary which makes it simple to pass in basic AppEvent information without using the more extensive methods below. The items arg\_dict looks for are as follows:

- "eventtype":(maps to string) The name of the event. This will autmatically be filled if nothing is passed in when you are sending and event with a stacktrace.
- "eventmessage":(maps to string) The message of the event. This will autmatically be filled if nothing is passed in when you are sending and event with a stacktrace.
- "user":(maps to string) User that triggered the event
- "session":(maps to string) Session that triggered the event
- "time":(maps to string) Time that the operation took (usually in miliseconds)
- "url":(maps to string) URL of the page the error occurred on
- "corrid":(maps to string) The correlation id
- "device":(maps to string) The machine name or type you are targeting

You can of course leave out anything you don't need, or pass in an empty dictionary to arg_dict if you don't wish to give any data



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
        appevent = client.create_new_app_event("FATAL", exc_info=True)

        #Populate any field with your own data, or send your own custom data
        appevent.context_app_browser = "Chrome"
        appevent.context_app_browser_version = "67.x"

        #Can support multiple ways to input data
        appevent.custom_properties = CustomData("Custom Data holder!")
        appevent.custom_properties.string_data = CustomStringData("Custom String Data 1",
                                                                  "Custom String Data 2")
        appevent.custom_properties.string_data.custom_data3 = "More Custom Data!"
        appevent.event_user = "john@traker.io"
        appevent.event_session = "6"

        appevent.context_operation_time_millis = 1000
        appevent.context_device = "pc"
        appevent.context_app_sku = "mobile"
        appevent.context_tags = ["client, frontend"]

        #Send it to trakerr
        client.send_event_async(appevent)

    return 0
```

create\_new\_app\_event's full signature is as follows: 
```python
create_new_app_event(self, log_level="error", classification="issue", event_type="unknown",
                     event_message="unknown", exc_info=False):
```
exc\_info can be set to `True` to get the latest exception traces from sys.exc\_info or simply passed in.

If you are using Django, we recommend that you look at [django user agents](https://github.com/selwin/django-user_agents) as a simple and quick way of getting the browser's name and version rather than parsing the user agent yourself. The library also allows you to check the client browser in the template, allowing you to modify the front end to the error accordingly. Please note that this library is _not maintained by or related to Trakerr in any way_.

## An in-depth look at TrakerrClient's properties
TrakerrClient's constructor initalizes the default values to all of TrakerrClient's properties.

```python
def __init__(self, api_key, context_app_version="1.0",
             context_deployment_stage="development", application_sku="", tags=[],
             threads=4, connnections=4):
```
The threads parameter specify the number of `max_workers` in the thread pool. This only matters if you are using `send_event_async` in python 3.2+. The connections parameter specificies the number of connections in the connection pool. If there are more threads than connections, the connection pool will block the derivitive async calls until it can serve a connection.

The TrakerrClient class however has a lot of exposed properties. The benefit to setting these immediately after after you create the TrakerrClient is that AppEvent will default it's values with the `TrakerrClient` instance that created it.
This way if there is a value that all your AppEvents uses, and the constructor default value currently doesn't suit you; it may be easier to change it in the `TrakerrClient` instance as it will become the default value for all AppEvents created after. A lot of these are populated by default value by the constructor, but you can populate them with whatever string data you want. The following table provides an in depth look at each of those.

If you're populating an app event directly, you'll want to take a look at the [AppEvent properties](generated/docs/AppEvent.md) as they contain properties unique to each AppEvent which do not have defaults you may set in the client.


Name | Type | Description | Notes
------------ | ------------- | -------------  | -------------
**api_key** | **string** | API key generated for the application. | 
**context_app\_version** | **string** | Application version information. | Default value: `1.0`
**context\_development\_stage** | **string** | One of development, staging, production; or a custom string. | Default Value: `development`
**context\_env\_anguage** | **string** | Constant string representing the language the application is in. | Default value: `python`
**context\_env\_name** | **string** | Name of the interpreter the program is run on. | Default Value: `platform.python_implementation()`
**context\_env\_version** | **string** | Version of python this program is running on. | Default Value: `platform.python_version()`
**context\_env\_hostname** | **string** | Hostname or ID of environment. | Default value: `platform.node()`
**context\_app\_os** | **string** | OS the application is running on. | Default value: `platform.system() + platform.release()` on Windows, `platform.system()` on all other platforms
**context\_appos\_version** | **string** | OS Version the application is running on. | Default value: `platform.version()` on Windows, `platform.release()` on all other platforms
**context\_appbrowser** | **string** | An optional string browser name the application is running on. | Defaults to `None`
**context\_appbrowser\_version** | **string** | An optional string browser version the application is running on. | Defaults to `None`
**context\_data\_center** | **string** | Data center the application is running on or connected to. | Defaults to `None`
**context\_data\_center\_region** | **string** | Data center region. | Defaults to `None`
**context\_app\_sku** | **str** | (optional) Application SKU | Defaults to `None`
**context_tags** | **str** | (optional) Application SKU | Defaults to `[]`

## Advanced pip install commands for Trakerr
You can run the following command to update an exsisting installation to the latest commit on master:
```bash
pip install git+https://github.com/trakerr-com/trakerr-python.git --upgrade
```

You can install from a branch for development or testing a new feature (Not recommended for production use):
```bash
pip install git+https://github.com/trakerr-com/trakerr-python.git@<branch_name_here>
```

## Documentation For Models

 - [AppEvent](https://github.com/trakerr-com/trakerr-python/blob/master/generated/docs/AppEvent.md)

## Author
[RM](https://github.com/RMSD)
