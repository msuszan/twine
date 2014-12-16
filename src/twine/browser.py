from spynner import *
from utils import make_boolean

class TwineBrowser(Browser):
    def __init__(self, debug_level):
        super(TwineBrowser, self).__init__(debug_level = debug_level)

        self.headers = [("Accept", "text/html; */*")]
        self._http_status = ""
        self._content_type = ""
        self._title = ""

        self._history = []

        # Keep track of old form values so they can be restored on formclear
        self._previous_form_values = {}

        # Last form modified by user
        # Used for default submit command
        self.last_form = None

        # Dictionary of dictionaries
        # Indexed first by url, and then by realm
        self._realmCredentials = {}

        # Dictionary indexed by url only
        # Used when a realm is not specified
        self._urlCredentials = {}

        self.set_http_authentication_callback(self.http_authentication_callback)

        self.at_empty_page = True

    @property
    def url(self):
        if self.at_empty_page:
            return ""
        else:
            return super(TwineBrowser, self).url

    @property
    def html(self):
        if self.at_empty_page:
            return ""
        else:
            return super(TwineBrowser, self).html

    @property
    def http_status(self):
        return self._http_status

    @property
    def content_type(self):
        return self._content_type

    @property
    def title(self):
        return self._title

    @property
    def history(self):
        return self._history

    def add_header(self, header):
        self.headers.append(header)

    def reset_headers(self):
        self.headers = [("Accept", "text/html; */*")]

    def add_credentials(self, realm, url, username, password):
        if realm:
            if url not in self._realmCredentials:
                self._realmCredentials[url] = {}
            self._realmCredentials[url][realm] = (username, password)
        else:
            self._urlCredentials[url] = (username, password)

    def http_authentication_callback(self, url, realm):
        realm_auth = self._realmCredentials.get(url)
        if realm_auth:
            realm_auth = realm_auth.get(realm)
        url_auth = self._urlCredentials.get(url)
        return realm_auth or url_auth

    def load(self, url, add_to_history = True):
        if url:
            old_url = self.url
            self._http_statuses = {}
            self._content_types = {}

            ret = super(TwineBrowser, self).load(url)

            if ret:
                if add_to_history and old_url:
                    self._history.append(old_url)
                self.at_empty_page = False
                self.last_form = None

                self._http_status = self._http_statuses.get(self.url, "")
                self._content_type = self._content_types.get(self.url, "")
                self._title =  self.soup("title").text() or ""

                self._previous_form_values = {}

                self.load_jquery(True)

            return ret
        else:
            self.at_empty_page = True
            return True

    def go(self, url):
        if url:
            try_urls = [url, ]

            # if this is an absolute URL that is just missing the 'http://' at
            # the beginning, try fixing that.
            if url.find('://') == -1:
                full_url = 'http://%s' % (url,)  # mimic browser behavior
                try_urls.append(full_url)

            # if this is a '?' or '/' URL, then assume that we want to tack it
            # onto the end of the current URL.
            try_urls.append(urlparse.urljoin(self.url, url))

            for u in try_urls:
                if self.load(u):
                    return True
            return False
        else:
            self.load("")
            return True

    def _on_reply(self, reply):
        super(TwineBrowser, self)._on_reply(reply)

        try:
            http_status = "%s" % toString(
            reply.attribute(QNetworkRequest.HttpStatusCodeAttribute))
        except:
            http_status = ""

        self._http_statuses[self._reply_url] = http_status

        try:
            content_type = "%s" % toString(
            reply.header(QNetworkRequest.ContentTypeHeader))
        except:
            content_type = ""

        self._content_types[self._reply_url] = content_type

    def _javascript_console_message(self, message, line, sourceid):
        self.javascript_message = message
        super(TwineBrowser, self)._javascript_console_message(message, line,
                                                              sourceid)

    def run_javascript(self, jscode):
        self.javascript_message = ""
        self.runjs(jscode)
        return self.javascript_message

    def back(self):
        if self._history:
            last_page = self._history.pop()
            self.load(last_page, False)
            return True
        else:
            self.load("")
            return False

    def find_form(self, formname):
        try:
            formname = int(formname)
            formname -= 1

            all_forms = [ i for i in self.soup("form").items() ]

            if len(all_forms) > formname:
                form = all_forms[formname]
            else:
                raise TwineAssertionError("no matching forms!")

        except ValueError:
            forms = [ i for i in self.soup("form[name='%s']" % formname).items() ]

            if len(forms) > 1:
                raise TwineAssertionError("multiple form matches")
            if forms:
                form = forms[0]
            else:
                raise TwineAssertionError("no matching forms!")

        return form

    def add_previous_form_value(self, formname, fieldname, value):
        if formname not in self._previous_form_values:
            self._previous_form_values[formname] = {}
        self._previous_form_values[formname][fieldname] = value

    def formvalue(self, formname, fieldname, value):
        form = self.find_form(formname)

        try:
            fieldname = int(fieldname)
            fieldname -= 1

            all_fields = [ i for i in form.find("input").items() ]
            all_fields.extend([ i for i in form.find("select").items() ])
            all_fields.extend([ i for i in form.find("textarea").items() ])

            if len(all_fields) > fieldname:
                field = all_fields[fieldname]
            else:
                raise TwineAssertionError("no field matches \"%d\"" % fieldname)

        except ValueError:
            for field_tag in ("input", "select", "textarea"):
                fields = [ i for i in form.find("%s[name=%s]" %
                    (field_tag, fieldname)).items() ]

                if fields:
                    matched_field_tag = field_tag
                    break
                #if len(fields) > 1:
                    #raise TwineAssertionError("multiple field matches")

                #if fields:
                    #field = fields[0]
                    #matched_field_tag = field_tag
                    #break

        if not fields:
            raise TwineAssertionError("no field matches \"%s\"" % fieldname)

        field_type = fields[0].attr.type
        if len(fields) > 1:
            for field in fields:
                if field.attr.type != field_type:
                    raise TwineAssertionError("field types do not match")

        field = fields[0]

        if matched_field_tag == "input":
            if field_type == "text" or field_type == "password":
                self.add_previous_form_value(formname, fieldname,
                                             field.attr.value or "")
                self.fill("input[name=%s]" % fieldname, value)
            elif field_type == "checkbox":
                self.add_previous_form_value(formname, fieldname,
                                             field.attr.checked or False)
                checked = make_boolean(value)
                if checked:
                    self.check("input[name=%s]" % fieldname)
                else:
                    self.uncheck("input[name=%s]" % fieldname)
            elif field_type == "radio":
                self.add_previous_form_value(formname, fieldname,
                                             field.attr.value)
                self.check("input[name=%s][value=%s]" % (fieldname, value,))
        elif matched_field_tag == "select":
            # TODO: add to previous form values
            self.select("option[value=%s]" % value)
        elif matched_field_tag == "textarea":
            self.add_previous_form_value(formname, fieldname,
                                         field.attr.value or "")
            self.fill("textarea[name=%s]" % fieldname, value)
        else:
            raise TwineAssertionError("Unknown field tag")

        # Keep track of last form modified
        self.last_form = formname

    def formclear(self, formname):
        for fieldname in self._previous_form_values[formname]:
            self.formvalue(formname, fieldname,
                           self._previous_form_values[formname][fieldname])
