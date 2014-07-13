from spynner import *

class TwillBrowser(Browser):
    def __init__(self, debug_level):
        super(TwillBrowser, self).__init__(debug_level = debug_level)
        self.http_status = ""
        self.history = []
        self.headers = [("Accept", "text/html; */*")]

    def load(self, url):
        self._http_statuses = {} 

        ret = super(TwillBrowser, self).load(url, headers = self.headers)

        if ret:
            self.history.append(self.url)
            self.http_status = self._http_statuses.get(self.url, "")

        return ret

    def go(self, url):
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

    def _on_reply(self, reply):
        super(TwillBrowser, self)._on_reply(reply)

        try:
            http_status = "%s" % toString(
            reply.attribute(QNetworkRequest.HttpStatusCodeAttribute))
        except:
            http_status = ""

        self._http_statuses[self._reply_url] = http_status

    def get_http_status(self):
        return self.http_status

    def get_history(self):
        return self.history

    def back(self):
        self.history.pop()
        if self.history:
            last_page = self.history[-1]
            return super(TwillBrowser, self).load(last_page,
                            headers = self.headers)
        else:
            super(TwillBrowser, self).load("",
                            headers = self.headers)
            return False

    def add_header(self, header):
        self.headers.append(header)

    def get_headers(self):
        return self.headers

    def reset_headers(self):
        self.headers = [("Accept", "text/html; */*")]
