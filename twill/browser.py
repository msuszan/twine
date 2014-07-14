from spynner import *

class TwillBrowser(Browser):
    def __init__(self, debug_level):
        super(TwillBrowser, self).__init__(debug_level = debug_level)
        self.headers = [("Accept", "text/html; */*")]
        self._http_status = ""
        self._history = []
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
