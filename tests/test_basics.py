from twine.commands import *
from twine import set_output
from StringIO import StringIO
from tempfile import TemporaryFile

class TestBasics:
    def setUp(self):
        self.output = StringIO()
        set_output(self.output)

        fp = TemporaryFile('rw')

        go('http://127.0.0.1:5000/')
    def tearDown(self):
        self.output.close()
    def test_reload(self):
        reload()
    def test_url(self):
        url('127.0.0.1:5000')
    def test_code(self):
        code('200')
    def test_follow(self):
        follow('link')
        url('127.0.0.1:5000/link')
    def test_find(self):
        find('Hello World!')
    def test_notfind(self):
        notfind('Goodbye')
    def test_back(self):
        follow('link')
        back()
        find('Hello World!')
    def test_show(self):
        show()
        assert 'Hello World!' in self.output.getvalue()
    def test_echo(self):
        echo('Testing echo')
        assert 'Testing echo' in self.output.getvalue()
    def test_save_html(self):
        save_html('temp.html')
        fp = open('temp.html')
        assert 'Hello World!' in fp.read()
        fp.close()
    def test_info(self):
        info()
        assert 'http://127.0.0.1:5000/' in self.output.getvalue()
        assert '200' in self.output.getvalue()
        assert 'text/html' in self.output.getvalue()
        assert 'Index' in self.output.getvalue()
