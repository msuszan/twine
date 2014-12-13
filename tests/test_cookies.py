from twine.commands import *
from twine import set_output
from StringIO import StringIO
from tempfile import TemporaryFile

class TestCookies:
    def setUp(self):
        self.output = StringIO()
        set_output(self.output)
    def tearDown(self):
        self.output.close()
        set_output(None)

        reset_browser()
    def test_show_cookies(self):
        go('http://127.0.0.1:5000/cookie')
        show_cookies()
        assert 'examplecookie=examplevalue' in self.output.getvalue()
    def test_save_cookies(self):
        go('http://127.0.0.1:5000/cookie')
        save_cookies('saved_cookies')
        fp = open('saved_cookies')
        contents = fp.read()
        assert 'examplecookie' in contents
        assert 'examplevalue' in contents
        fp.close()
    def test_load_cookies(self):
        load_cookies('example_cookies_file')
        show_cookies()
        assert 'examplecookie=examplevalue' in self.output.getvalue()
