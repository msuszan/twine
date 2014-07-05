"""
Implementation of all of the individual 'twill' commands available through
twill-sh.
"""

import sys

OUT=None
ERR=sys.stderr

# export:
__all__ = ['get_browser',
           'reset_browser',
           'extend_with',
           'exit',
           'go',
           'reload',
           'url',
           'code',
           'follow',
           'find',
           'notfind',
           'back',
           'show',
           'echo',
           'save_html',
           'sleep',
           'agent',
           'showforms',
           'showlinks',
           'showhistory',
           'submit',
           'formvalue',
           #'fv',
           'formaction',
           #'fa',
           'formclear',
           'formfile',
           'getinput',
           'getpassword',
           'save_cookies',
           'load_cookies',
           'clear_cookies',
           'show_cookies',
           'add_auth',
           'run',
           'runfile',
           'setglobal',
           'setlocal',
           'debug',
           'title',
           'exit',
           'config',
           'tidy_ok',
           'redirect_output',
           'reset_output',
           'redirect_error',
           'reset_error',
           'add_extra_header',
           'show_extra_headers',
           'clear_extra_headers',
           'info'
           ]

import re, getpass, time

from errors import TwillException, TwillAssertionError
import utils
from utils import set_form_control_value, run_tidy
from namespaces import get_twill_glocals

import spynner
import pyquery
import urlparse

browser = spynner.Browser(debug_level = spynner.ERROR)
browser.set_html_parser(pyquery.PyQuery)
        
def get_browser():
    return browser

def reset_browser():
    """
    >> reset_browser

    Reset the browser completely.
    """
    global browser

    browser = spynner.Browser(debug_level = spynner.ERROR)
    browser.set_html_parser(pyquery.PyQuery)

def exit(code = "0"):
    """
    exit [<code>]

    Exits twill, with the given exit code (defaults to 0, "no error").
    """
    raise SystemExit(int(code))

def go(url):
    """
    >> go <url>
    
    Visit the URL given.
    """
    try_urls = [url, ]

    # if this is an absolute URL that is just missing the 'http://' at
    # the beginning, try fixing that.
    if url.find('://') == -1:
        full_url = 'http://%s' % (url,)  # mimic browser behavior
        try_urls.append(full_url)

    # if this is a '?' or '/' URL, then assume that we want to tack it onto
    # the end of the current URL.
    try_urls.append(urlparse.urljoin(browser.url, url))
    
    success = False
    for u in try_urls:
        if browser.load(u):
            success = True
            break

    if success:
        print>>OUT, '==> at', browser.url
    else:
        raise TwillException("cannot go to '%s'" % (url,))

    return browser.url

def reload():
    """
    >> reload
    
    Reload the current URL.
    """
    browser.load(browser.url)
    print>>OUT, '==> reloaded'

def code(should_be):
    """
    >> code <int>
    
    Check to make sure the response code for the last page is as given.
    """
    raise TwillAssertionError("Not yet implemented")

def tidy_ok():
    """
    >> tidy_ok

    Assert that 'tidy' produces no warnings or errors when run on the current
    page.

    If 'tidy' cannot be run, will fail silently (unless 'tidy_should_exist'
    option is true; see 'config' command).
    """
    raise TwillAssertionError("Not yet implemented")

def url(should_be):
    """
    >> url <regexp>

    Check to make sure that the current URL matches the regexp.  The local
    variable __match__ is set to the matching part of the URL.
    """
    regexp = re.compile(should_be)
    current_url = browser.url

    m = None
    if current_url is not None:
        m = regexp.search(current_url)
    else:
        current_url = ''

    if not m:
        raise TwillAssertionError("""\
current url is '%s';
does not match '%s'
""" % (current_url, should_be,))

    if m.groups():
        match_str = m.group(1)
    else:
        match_str = m.group(0)

    global_dict, local_dict = get_twill_glocals()
    local_dict['__match__'] = match_str
    return match_str

def follow(what):
    """
    >> follow <regexp>
    
    Find the first matching link on the page & visit it.
    """
    raise TwillAssertionError("Not yet implemented")

def _parseFindFlags(flags):
    KNOWN_FLAGS = {
        'i': re.IGNORECASE,
        'm': re.MULTILINE,
        's': re.DOTALL,
        }
    finalFlags = 0
    for char in flags:
        try:
            finalFlags |= KNOWN_FLAGS[char]
        except IndexError:
            raise TwillAssertionError("unknown 'find' flag %r" % char)
    return finalFlags

def find(what, flags=''):
    """
    >> find <regexp> [<flags>]
    
    Succeed if the regular expression is on the page.  Sets the local
    variable __match__ to the matching text.

    Flags is a string consisting of the following characters:

    * i: ignorecase
    * m: multiline
    * s: dotall

    For explanations of these, please see the Python re module
    documentation.
    """
    regexp = re.compile(what, _parseFindFlags(flags))
    page = browser.html

    m = regexp.search(page)
    if not m:
        raise TwillAssertionError("no match to '%s'" % (what,))

    if m.groups():
        match_str = m.group(1)
    else:
        match_str = m.group(0)

    _, local_dict = get_twill_glocals()
    local_dict['__match__'] = match_str

def notfind(what, flags=''):
    """
    >> notfind <regexp> [<flags>]
    
    Fail if the regular expression is on the page.
    """
    regexp = re.compile(what, _parseFindFlags(flags))
    page = browser.html

    if regexp.search(page):
        raise TwillAssertionError("match to '%s'" % (what,))

def back():
    """
    >> back
    
    Return to the previous page.
    """
    raise TwillAssertionError("Not yet implemented")

def show():
    """
    >> show
    
    Show the HTML for the current page.
    """
    html = browser.html
    print>>OUT, html
    return html

def echo(*strs):
    """
    >> echo <list> <of> <strings>
    
    Echo the arguments to the screen.
    """
    strs = map(str, strs)
    s = " ".join(strs)
    print>>OUT, s

def save_html(filename=None):
    """
    >> save_html [<filename>]
    
    Save the HTML for the current page into <filename>.  If no filename
    given, construct the filename from the URL.
    """
    html = browser.html
    if html is None:
        print>>OUT, "No page to save."
        return

    if filename is None:
        url = b.url
        url = url.split('?')[0]
        filename = url.split('/')[-1]
        if filename is "":
            filename = 'index.html'

        print>>OUT, "(Using filename '%s')" % (filename,)

    f = open(filename, 'w')
    f.write(html)
    f.close()

def sleep(interval=1):
    """
    >> sleep [<interval>]

    Sleep for the specified amount of time.
    If no interval is given, sleep for 1 second.
    """
    time.sleep(float(interval))

_agent_map = dict(
    ie5='Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 5.1)',
    ie55='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.1)',
    ie6='Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    moz17='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7) Gecko/20040616',
    opera7='Opera/7.0 (Windows NT 5.1; U) [en]',
    konq32='Mozilla/5.0 (compatible; Konqueror/3.2.3; Linux 2.4.14; X11; i686)',
    saf11='Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/100 (KHTML, like Gecko) Safari/100',
    aol9='Mozilla/4.0 (compatible; MSIE 5.5; AOL 9.0; Windows NT 5.1)',)

def agent(what):
    """
    >> agent <agent>
    
    Set the agent string (identifying the browser brand).

    Some convenient shortcuts:
      ie5, ie55, ie6, moz17, opera7, konq32, saf11, aol9.
    """
    raise TwillAssertionError("Not yet implemented")

def submit(submit_button=None):
    """
    >> submit [<buttonspec>]
    
    Submit the current form (the one last clicked on) by clicking on the
    n'th submission button.  If no "buttonspec" is given, submit the current
    form by using the last clicked submit button.

    The form to submit is the last form clicked on with a 'formvalue' command.

    The button used to submit is chosen based on 'buttonspec'.  If 'buttonspec'
    is given, it's matched against buttons using the same rules that
    'formvalue' uses.  If 'buttonspec' is not given, submit uses the last
    submit button clicked on by 'formvalue'.  If none can be found,
    submit submits the form with no submit button clicked.
    """
    raise TwillAssertionError("Not yet implemented")

def showforms():
    """
    >> showforms
    
    Show all of the forms on the current page.
    """
    raise TwillAssertionError("Not yet implemented")

def showlinks():
    """
    >> showlinks
    
    Show all of the links on the current page.
    """
    for n, link in enumerate(browser.soup("a").items()):
        print>>OUT, "%d. %s ==> %s" % (n, link.text(), link.attr("href"),)
    print>>OUT, ''

def showhistory():
    """
    >> showhistory

    Show the browser history (what URLs were visited).
    """
    raise TwillAssertionError("Not yet implemented")
    
def formclear(formname):
    """
    >> formclear <formname>
    
    Run 'clear' on all of the controls in this form.
    """
    raise TwillAssertionError("Not yet implemented")

#fv = formvalue

def formvalue(formname, fieldname, value):
    """
    >> formvalue <formname> <field> <value>

    Set value of a form field.

    There are some ambiguities in the way formvalue deals with lists:
    'formvalue' will *add* the given value to a list of multiple selection,
    for lists that allow it.

    Forms are matched against 'formname' as follows:
      1. regexp match to actual form name;
      2. if 'formname' is an integer, it's tried as an index.

    Form controls are matched against 'fieldname' as follows:
      1. unique exact match to control name;
      2. unique regexp match to control name;
      3. if fieldname is an integer, it's tried as an index;
      4. unique & exact match to submit-button values.

    Formvalue ignores read-only fields completely; if they're readonly,
    nothing is done, unless the config options ('config' command) are
    changed.

    'formvalue' is available as 'fv' as well.
    """
    raise TwillAssertionError("Not yet implemented")

#fa = formaction

def formaction(formname, action):
    """
    >> formaction <formname> <action_url>

    Sets action parameter on form to action_url
    """
    raise TwillAssertionError("Not yet implemented")

def formfile(formname, fieldname, filename, content_type=None):
    """
    >> formfile <form> <field> <filename> [ <content_type> ]

    Upload a file via an "upload file" form field.
    """
    raise TwillAssertionError("Not yet implemented")

def extend_with(module_name):
    """
    >> extend_with <module>
    
    Import contents of given module.
    """
    raise TwillAssertionError("Not yet implemented")

def getinput(prompt):
    """
    >> getinput <prompt>
    Get input, store it in '__input__'.
    """
    raise TwillAssertionError("Not yet implemented")

def getpassword(prompt):
    """
    >> getpassword <prompt>
    
    Get a password ("invisible input"), store it in '__password__'.
    """
    raise TwillAssertionError("Not yet implemented")

def save_cookies(filename):
    """
    >> save_cookies <filename>

    Save all of the current cookies to the given file.
    """
    raise TwillAssertionError("Not yet implemented")

def load_cookies(filename):
    """
    >> load_cookies <filename>

    Clear the cookie jar and load cookies from the given file.
    """
    raise TwillAssertionError("Not yet implemented")

def clear_cookies():
    """
    >> clear_cookies

    Clear the cookie jar.
    """
    raise TwillAssertionError("Not yet implemented")

def show_cookies():
    """
    >> show_cookies

    Show all of the cookies in the cookie jar.
    """
    raise TwillAssertionError("Not yet implemented")

def add_auth(realm, uri, user, passwd):
    """
    >> add_auth <realm> <uri> <user> <passwd>

    Add HTTP Basic Authentication information for the given realm/uri.

    Note: realms are not currently supported; <realm> is ignored.
    """
    raise TwillAssertionError("Not yet implemented")

def debug(what, level):
    """
    >> debug <what> <level>

    <what> can be:
       * http (any level >= 1), to display the HTTP transactions.
       * commands (any level >= 1), to display the commands being executed.
       * equiv-refresh (any level >= 1) to display HTTP-EQUIV refresh handling.
    """
    raise TwillAssertionError("Not yet implemented")

def run(cmd):
    """
    >> run <command>

    <command> can be any valid python command; 'exec' is used to run it.
    """
    raise TwillAssertionError("Not yet implemented")

def runfile(*files):
    """
    >> runfile <file1> [ <file2> ... ]

    """
    raise TwillAssertionError("Not yet implemented")

def setglobal(name, value):
    """
    setglobal <name> <value>

    Sets the variable <name> to the value <value> in the global namespace.
    """
    raise TwillAssertionError("Not yet implemented")

def setlocal(name, value):
    """
    setlocal <name> <value>

    Sets the variable <name> to the value <value> in the local namespace.
    """
    raise TwillAssertionError("Not yet implemented")

def title(what):
    """
    >> title <regexp>
    
    Succeed if the regular expression is in the page title.
    """
    regexp = re.compile(what)
    title = browser.title

    print>>OUT, "title is '%s'." % (title,)

    m = regexp.search(title)
    if not m:
        raise TwillAssertionError("title does not contain '%s'" % (what,))

def redirect_output(filename):
    """
    >> redirect_output <filename>

    Append all twill output to the given file.
    """
    raise TwillAssertionError("Not yet implemented")

def reset_output():
    """
    >> reset_output

    Reset twill output to go to the screen.
    """
    raise TwillAssertionError("Not yet implemented")

def redirect_error(filename):
    """
    >> redirect_error <filename>

    Append all twill error output to the given file.
    """
    raise TwillAssertionError("Not yet implemented")

def reset_error():
    """
    >> reset_error
    
    Reset twill error output to go to the screen.
    """
    raise TwillAssertionError("Not yet implemented")

def add_extra_header(header_key, header_value):
    """
    >> add_header <name> <value>

    Add an HTTP header to each HTTP request.  See 'show_extra_headers' and
    'clear_extra_headers'.
    """
    raise TwillAssertionError("Not yet implemented")

def show_extra_headers():
    """
    >> show_extra_headers

    Show any extra headers being added to each HTTP request.
    """
    raise TwillAssertionError("Not yet implemented")

def clear_extra_headers():
    """
    >> clear_extra_headers

    Remove all user-defined HTTP headers.  See 'add_extra_header' and
    'show_extra_headers'.
    """
    raise TwillAssertionError("Not yet implemented")

def config(key=None, value=None):
    """
    >> config [<key> [<int value>]]

    Configure/report various options.  If no <value> is given, report
    the current key value; if no <key> given, report current settings.

    So far:

     * 'acknowledge_equiv_refresh', default 1 -- follow HTTP-EQUIV=REFRESH
     * 'readonly_controls_writeable', default 0 -- make ro controls writeable
     * 'require_tidy', default 0 -- *require* that tidy be installed
     * 'use_BeautifulSoup', default 1 -- use the BeautifulSoup parser
     * 'use_tidy', default 1 -- use tidy, if it's installed
     * 'with_default_realm', default 0 -- use a default realm for HTTP AUTH

    Deprecated:
     * 'allow_parse_errors' has been removed.
    """
    raise TwillAssertionError("Not yet implemented")

def info():
    """
    >> info

    Report information on current page.
    """
    raise TwillAssertionError("Not yet implemented")
