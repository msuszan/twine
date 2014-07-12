from spynner import *

class TwillBrowser(Browser):
    def __init__(self, debug_level):
        super(TwillBrowser, self).__init__(debug_level)
        self.http_status = ""

    def load(self, url, headers):
        self.http_status = ""
        return super(TwillBrowser, self).load(url, headers = headers)

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
