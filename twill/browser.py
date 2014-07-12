from spynner import *

class TwillBrowser(Browser):
    def __init__(self, debug_level):
        super(TwillBrowser, self).__init__(debug_level)
        self.http_status = ""
        self.history = []
        self.request_headers = [("Accept", "text/html; */*")]

    def load(self, url):
        self.http_status = ""
        old_url = self.url

        ret = super(TwillBrowser, self).load(url,
                            headers = self.request_headers)

        if ret:
            self.history.append(self.url)

        print self.history

        return ret

    def _on_reply(self, reply):
        super(TwillBrowser, self)._on_reply(reply)

        if self._reply_url == self.url:
            try:
                http_status = "%s" % toString(
                reply.attribute(QNetworkRequest.HttpStatusCodeAttribute))
            except:
                http_status = ""

            self.http_status = http_status

    def get_http_status(self):
        return self.http_status

    def get_history(self):
        return self.history

    def back(self):
        self.history.pop()
        if self.history:
            last_page = self.history[-1]
            return super(TwillBrowser, self).load(last_page,
                            headers = self.request_headers)
        else:
            super(TwillBrowser, self).load("",
                            headers = self.request_headers)
            return False
