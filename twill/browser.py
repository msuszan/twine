from spynner import *

class TwillBrowser(Browser):
    def __init__(self, debug_level):
        super(TwillBrowser, self).__init__(debug_level = debug_level)
        self.headers = [("Accept", "text/html; */*")]
        self._http_status = ""
        self._history = []

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
            return super(TwillBrowser, self).url

    @property
    def html(self):
        if self.at_empty_page:
            return ""
        else:
            return super(TwillBrowser, self).html

    @property
    def http_status(self):
        return self._http_status

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

            ret = super(TwillBrowser, self).load(url)

            if ret:
                self._http_status = self._http_statuses.get(self.url, "")
                if add_to_history and old_url:
                    self._history.append(old_url)
                self.at_empty_page = False

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
        super(TwillBrowser, self)._on_reply(reply)

        print self._reply_url

        try:
            http_status = "%s" % toString(
            reply.attribute(QNetworkRequest.HttpStatusCodeAttribute))
        except:
            http_status = ""

        self._http_statuses[self._reply_url] = http_status

    def back(self):
        if self._history:
            last_page = self._history.pop()
            self.load(last_page, False)
            return True
        else:
            self.load("")
            return False
