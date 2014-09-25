"""
twine Web testing language & associated utilities.
"""

__version__ = "1.8.0"

__all__ = [ "TwineCommandLoop",
            "execute_file",
            "execute_string",
            "get_browser",
            "add_wsgi_intercept",
            "remove_wsgi_intercept",
            "set_output",
            "set_errout"]

#
# add extensions (twine/extensions) and the the wwwsearch & pyparsing
# stuff from twine/included-packages/.  NOTE: this works with eggs! hooray!
#

import sys, os.path
thisdir = os.path.dirname(__file__)

# add extensions directory at the *end* of sys.path.  This means that
# user extensions will take priority over twine extensions.
extensions = os.path.join(thisdir, 'extensions')
sys.path.append(extensions)

# add other_packages in at the *beginning*, so that the correct
# (patched) versions of pyparsing and mechanize get imported.
wwwsearchlib = os.path.join(thisdir, 'other_packages')
sys.path.insert(0, wwwsearchlib)

# the two core components of twine:
from shell import TwineCommandLoop
from parse import execute_file, execute_string

# convenience function or two...
from commands import get_browser

def get_browser_state():
    import warnings
    warnings.warn("""\
get_browser_state is deprecated; use 'twine.get_browser() instead.
""", DeprecationWarning)
    return get_browser()

# initialize global dict
import namespaces
namespaces.init_global_dict()

from wsgi_intercept import add_wsgi_intercept, remove_wsgi_intercept

def set_output(fp):
    """
    Have standard output from twine go to the given fp instead of
    stdout.  fp=None will reset to stdout.
    """
    import commands, browser
    commands.OUT = browser.OUT = fp

def set_errout(fp):
    """
    Have error output from twine go to the given fp instead of stderr.
    fp=None will reset to stderr.
    """
    import commands
    if fp:
        commands.ERR = fp
    else:
        commands.ERR = sys.stderr
