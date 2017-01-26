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
import trakerr_client
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

    logger = Trakerr.getLogger("<API Key here>", "App version here", "Name for the current logger")

    try:
        raise ArithmeticError()
    except:
       logger.exception("Bad math.")
```
### Option 2: Manual initialization of the handler
You can initialize the handler directly and attach it to your own logger, if you want direct control over it. This is useful if you want your own custom logger. An example with the base logger follows.

You'll need to add these imports:
```python
import logging
from trakerr_handler import TrakerrHandler
```

And then you'll need to create a handler and a logger object and attach them before you can use them later on.
```python
def main(argv=None):
    logger = logging.getLogger("Logger name")
    th = TrakerrHandler("API Key here", "App Version Number")
    logger.addHandler(th)

    try:
        raise ArithmeticError()
    except:
       logger.exception("Bad math.")
```

### Option 3: Direct Access to the Trakerr layer
You can bypass the handler altogether and use the underlying TrakerrAPI to send an event. This will allow you to send an event with a bit more control over the event data that will be sent. The example following is simple, so be sure to check the log method documentation (in trakerr__client.py) and method header!

```python
from trakerr__client import Trakerr
```

Once you've imported trakerr, you can simply instantiate the class and call log, or pass more info into the function.

```python
def main(argv=None):
    if argv is None:
        argv = sys.argv

    l = TrakerrSend("API Key here", "App Version Number")
    try:
        raise EnvironmentError("Test Bug.")
    except:
        l.log()
```

## Documentation For Models

 - [AppEvent](https://github.com/trakerr-io/trakerr-python/blob/master/generated/docs/AppEvent.md)

## Author
RM


