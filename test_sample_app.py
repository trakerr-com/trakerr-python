
import sys
import os
import re
import traceback


#Normal automatic instantiation
from trakerr import Trakerr


"""
#With handler, manual init
import logging
from trakerr import TrakerrHandler
"""


def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    logger = Trakerr.getLogger("API KEY", "App Version number here", "Name")

    try:
        raise FloatingPointError()
    except:
       logger.exception("Bad math.")

    return 0
    
    """
    #Manual instantiation of the logger.
    logger = logging.getLogger("Logger name")
    th = TrakerrHandler("API KEY", "App Version number here")
    logger.addHandler(th)

    try:
        raise ArithmeticError()
    except:
       logger.exception("Bad math.")

    return 0
    """


if __name__ == "__main__":
    #main()
    sys.exit(main())