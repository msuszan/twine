from twine.commands import *
from twine import set_output
from StringIO import StringIO
from tempfile import TemporaryFile

class TestFormValue:
    def setUp(self):
        self.output = StringIO()
        set_output(self.output)

        go('http://127.0.0.1:5000/form')
    def tearDown(self):
        self.output.close()
        set_output(None)

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
    def test_checked_checkbox_field(self):
        formvalue('1', 'accept_tos', 'true')
        submit()
        find('You accepted the TOS')
    def test_unchecked_checkbox_field(self):
        formvalue('1', 'accept_tos', 'false')
        submit()
        find('You rejected the TOS')
    def test_formaction(self):
        formaction('1', '/alternate_form')
        formvalue('1', 'name', 'examplename')
        submit()
        find('Your name is examplename')
        url('alternate_form')
    def test_showforms_basic(self):
        showforms()
        assert 'name' in self.output.getvalue()
        assert 'password' in self.output.getvalue()
        assert 'gender' in self.output.getvalue()
        assert 'language' in self.output.getvalue()
        assert 'comments' in self.output.getvalue()
        assert 'accept_tos' in self.output.getvalue()
        assert 'submit' in self.output.getvalue()
    def test_showforms_text_field(self):
        formvalue('1', 'name', 'examplename')
        showforms()
        assert 'examplename' in self.output.getvalue()
    def test_showforms_password_field(self):
        formvalue('1', 'password', 'examplepassword')
        showforms()
        assert 'examplepassword' in self.output.getvalue()
