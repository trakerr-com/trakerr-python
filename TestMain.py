
import sys
import os
import re
import traceback

from trakerr__client import Trakerr



def main(argv=None):#Test Main, to be removed
    if argv is None:
        argv = sys.argv

    try:
        raise EnvironmentError("Test Bug.")
    except:
        l.log()
        


if __name__ == "__main__":
    main()
#    sys.exit(main())