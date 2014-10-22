from twine.commands import *

class TestBasics:
    def setUp(self):
        go('http://127.0.0.1:5000/')
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
