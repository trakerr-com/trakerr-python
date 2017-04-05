# Trakerr-python API client
Get your application events and errors to Trakerr via the *Trakerr API*.

You will need your API key to send events to trakerr.

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

To install from master, simply use:
```sh
pip install git+https://github.com/trakerr-io/trakerr-python.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/trakerr-io/trakerr-python.git`)

You can run the following command to update an exsisting installation to the latest commit on master:
```sh
pip install git+https://github.com/trakerr-io/trakerr-python.git --upgrade
```

You can install from a branch (Not recommended for production use):
```sh
pip install git+https://github.com/trakerr-io/trakerr-python.git#<branch_name_here>
```

Then import the package in your code:
```python
import trakerr
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and you're set to add Trakerr to your project. All of these examples are included in test_sample_app.py.

### Option 1: Automatic initialization of the python logger
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

### Option 2: Manual initialization of the handler, attach it to a python logger
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


### Sending an error(or non-error) quickly without using the logger
You can quickly send a simple event with partial custom data from the log function of the `TrakerrClient`. Add these imports:

```python
from trakerr import TrakerrClient
```

you can then send call log simply to send a quick error to Trakerr. Note the values that the argument dictionary takes are in the log docstring.

```python
client = TrakerrClient("API Key here", "App Version number")

client.log({"user":"jill@trakerr.io", "session":"25", "errname":"user logon issue",
            "errmessage":"User refreshed the page."}, "info", "logon script", False)
```

You can call this from an `except` if you wish to send an error with a stacktrace.

### Option 4: Add Custom Data
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
        
        #You can use this call to create an app event
        #appevent = client.create_new_app_event("ERROR", "Index Error", "Math")
        #without a stacktrace, in case you do don't have a stacktrace or you're not sending a crash.

        #Populate any field with your own data, or send your own custom data
        appevent.context_app_os = "Windows 8"
        appevent.custom_properties = CustomData("Custom Data holder!")
        
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

## An in-depth look at TrakerrClient's properties
TrakerrClient's constructor initalizes the default values to all of TrakerrClient's properties.

```python
def __init__(self, api_key, context_app_version = "1.0", context_deployment_stage =  "development"):
```

The TrakerrClient class however has a lot of exposed properties. The benefit to setting these immediately after after you create the TrakerrClient is that AppEvent will default it's values against the TrakerClient that created it. This way if there is a value that all your AppEvents uses, and the constructor default value currently doesn't suit you; it may be easier to change it in TrakerrClient as it will become the default value for all AppEvents created after. A lot of these are populated by default value by the constructor, but you can populate them with whatever string data you want. The following table provides an in depth look at each of those.


Name | Type | Description | Notes
------------ | ------------- | -------------  | -------------
**apiKey** | **string** | API key generated for the application | 
**contextAppVersion** | **string** | Application version information. | Default value: "1.0" 
**contextDevelopmentStage** | **string** | One of development, staging, production; or a custom string. | Default Value: "develoment"
**contextEnvLanguage** | **string** | Constant string representing the language the application is in. | Default value: "python"
**contextEnvName** | **string** | Name of the interpreter the program is run on. | Default Value: `platform.python_implementation()`
**contextEnvVersion** | **string** | Version of python this program is running on. | Default Value: `platform.python_version()`
**contextEnvHostname** | **string** | Hostname or ID of environment. | Default value: `platform.node()`
**contextAppOS** | **string** | OS the application is running on. | Default value: `platform.system() + platform.release()`
**contextAppOSVersion** | **string** | OS Version the application is running on. | Default value: `platform.version()`
**contextAppOSBrowser** | **string** | An optional string browser name the application is running on. | Defaults to `None`
**contextAppOSBrowserVersion** | **string** | An optional string browser version the application is running on. | Defaults to `None`
**contextDataCenter** | **string** | Data center the application is running on or connected to. | Defaults to `None`
**contextDataCenterRegion** | **string** | Data center region. | Defaults to `None`


The server accepts the final two arguments before url_path, but they are currently in development on this api level, so if you are using django or another web framework; please use the REST API. They are not currently available in the `TrakerrClient` constructor.


## Documentation For Models

 - [AppEvent](https://github.com/trakerr-io/trakerr-python/blob/master/generated/docs/AppEvent.md)

## Author
[RM](https://github.com/RMSD)
