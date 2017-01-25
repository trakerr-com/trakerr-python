# trakerr_client
Get your application events and errors to Trakerr via the *Trakerr API*.

This Python package is automatically generated by the [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) project:

- API version: 1.0.0
- Package version: 1.0.0
- Build date: 2016-11-30T15:05:52.105-08:00
- Build package: class io.swagger.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import trakerr_client
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import trakerr_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and you're set to add Trakerr to your project. All of these examples are included in testmain.py.

### Option one: Automatic initialization
Along with your imports, add:

```python
from trakerr import Trakerr
```

And then you can get a python logger object that ties in to trakerr to handle the various levels of errors, giving the appropriate data as strings. 

```python
def main(argv=None):
    if argv is None:
        argv = sys.argv

    logger = Trakerr.getLogger("API Key here", "App version here", "Name for the current logger")

    try:
        raise ArithmeticError()
    except:
       logger.exception("Bad math.")
```
### Option two: Manual initialization of the handler
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

### Option three: Direct Access to the Trakerr layer
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
## Documentation for API Endpoints

All URIs are relative to *https://www.trakerr.io/api/v1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*EventsApi* | [**events_post**](docs/EventsApi.md#events_post) | **POST** /events | Submit an application event or error to Trakerr


## Documentation For Models

 - [AppEvent](docs/AppEvent.md)
 - [CustomData](docs/CustomData.md)
 - [CustomDoubleData](docs/CustomDoubleData.md)
 - [CustomStringData](docs/CustomStringData.md)
 - [Error](docs/Error.md)
 - [InnerStackTrace](docs/InnerStackTrace.md)
 - [StackTraceLine](docs/StackTraceLine.md)
 - [StackTraceLines](docs/StackTraceLines.md)
 - [Stacktrace](docs/Stacktrace.md)


## Documentation For Authorization

 All endpoints do not require authorization.


## Author
RM


