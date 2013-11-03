# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2013, Hartmut Goebel <h.goebel@crazy-compilers.com>

import os
import logging
import sys

LOG_FORMAT =('%(levelname)s %(name)s '
             '%(asctime)s %(message)s '
             '(%(filename)s:%(lineno)s)')

ENV_VAR_NAME = 'COHERENCE_DEBUG'

#copy-pasted from "logging"
if hasattr(sys, 'frozen'): #support for py2exe
    _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

#copy-pasted from "logging"
def currentframe():
    import sys
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back

class Logger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        logging.Logger.__init__(self, name, level)
        pass

#copy-pasted from "logging"
    def findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == logging._srcfile or filename == _srcfile:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv

class Loggable(logging.Logger):
    """
    Base class for objects that want to be able to log messages with
    different level of severity.  The levels are, in order from least
    to most: log, debug, info, warning, error.

    @cvar logCategory: Implementors can provide a category to log their
       messages under.
    """

    logCategory = 'default'
    def __init__(self):
        pass

    def logObjectName(self):
        """Overridable object name function."""
        # cheat pychecker
        for name in ['logName', 'name']:
            if hasattr(self, name):
                return getattr(self, name)

        return None

    def log(self, message, *args, **kwargs):
        logging.getLogger(self.logCategory).log(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        logging.getLogger(self.logCategory).warning(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        logging.getLogger(self.logCategory).info(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        logging.getLogger(self.logCategory).critical(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        logging.getLogger(self.logCategory).debug(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        logging.getLogger(self.logCategory).error(message, *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        logging.getLogger(self.logCategory).exception(message, *args, **kwargs)

    fatal = critical
    warn = warning
    msg = info


def init(logfilename=None, loglevel=logging.WARN):
    logger = logging.getLogger()
    logging.addLevelName(100, 'NONE')

    logging.Logger.manager.setLoggerClass(Logger)

    logging.basicConfig(filename=logfilename, level=loglevel,
                        format=LOG_FORMAT)

    if ENV_VAR_NAME in os.environ:
        logger.setLevel(os.environ[ENV_VAR_NAME])
    else:
        logger.setLevel(loglevel)
