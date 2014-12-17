from twine.commands import *
from twine import set_output
from StringIO import StringIO
from tempfile import TemporaryFile

class TestFormValue:
    def setUp(self):
        go('http://127.0.0.1:5000/form')
    def tearDown(self):
        reset_browser()
    def test_text_field(self):
        formvalue('1', 'name', 'examplename')
        submit()
        find('Your name is examplename')
    def test_password_field(self):
        formvalue('1', 'password', 'examplepassword')
        submit()
        find('Your password is examplepassword')
    def test_radio_field(self):
        formvalue('1', 'gender', 'male')
        submit()
        find('Your gender is male')
    def test_select_field(self):
        formvalue('1', 'language', 'py')
        submit()
        find('Your language is py')
    def test_textarea_field(self):
        formvalue('1', 'comments', 'examplecomment')
        submit()
        find('You had the following comments: examplecomment')
    def test_formaction(self):
        formaction('1', '/alternate_form')
        formvalue('1', 'name', 'examplename')
        submit()
        find('examplename')
        url('alternate_form')
