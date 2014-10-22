from twine.commands import *
from test_server import test_server

class TestBasics:
    def setUp(self):
        go('http://127.0.0.1:5000/')
    def test_find(self):
        find('Hello World!')
    def test_code(Self):
        code('200')
