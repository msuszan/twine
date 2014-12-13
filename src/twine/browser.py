from spynner import *

class TwineBrowser(Browser):
    def __init__(self, debug_level):
        super(TwineBrowser, self).__init__(debug_level = debug_level)

        self.headers = [("Accept", "text/html; */*")]
        self._http_status = ""
        self._content_type = ""
        self._title = ""

        self._history = []

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
