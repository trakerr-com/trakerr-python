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
    
    logger = Trakerr.getLogger("API KEY", "App Version number here", "Name")

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
You can send custom data as part of your error event if you need to. Add these imports:
```python
from trakerr import TrakerrClient
from trakerr_client.models import CustomData, CustomStringData
```

You'll then need to initialize custom properties once you create the event. Note that you can use the second call commented out to instead creat an app event without a stacktrace.

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

## Documentation For Models

 - [AppEvent](https://github.com/trakerr-io/trakerr-python/blob/master/generated/docs/AppEvent.md)

## Author
RM


