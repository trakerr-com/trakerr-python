
import sys
import os
import re
import traceback


#Normal automatic instantiation
from trakerr import Trakerr

"""
#With handler, manual init
import logging
from trakerr_handler import TrakerrHandler
"""

"""
#Without handler
from trakerr__client import Trakerr
"""



def main(argv=None):
    if argv is None:
        argv = sys.argv

    logger = Trakerr.getLogger("API Key here", "App version here", "Name for the current logger")

    try:
        raise ArithmeticError()
    except:
       logger.exception("Bad math.")

    """
    #Manual instantiation of the logger.
    logger = logging.getLogger("Logger name")
    th = TrakerrHandler("API Key here", "App Version Number")
    logger.addHandler(th)

    try:
        raise ArithmeticError()
    except:
       logger.exception("Bad math.")
    """

    """
    #Without handler.
    l = TrakerrSend("API Key here", "App Version Number")
    try:
        raise EnvironmentError("Test Bug.")
    except:
        l.log()
        
    """
        


if __name__ == "__main__":
    main()
#    sys.exit(main())