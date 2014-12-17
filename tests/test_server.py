from flask import Flask, request, render_template, make_response
from wtforms import Form, validators
from wtforms import TextField, PasswordField, BooleanField, RadioField
from wtforms import SelectField, TextAreaField

class ContrivedForm(Form):
    name = TextField('Name', [validators.Optional()])

    password = PasswordField('Password', [validators.Optional()])

    gender = RadioField('Gender', choices=[('male','Male'),
        ('female','Female')], default='male')

    language_choices = [
        ('cpp', 'C++'),
        ('py', 'Python'),
        ('js', 'JavaScript')
    ]
    language = SelectField('Programming Language', choices=language_choices)

    comments = TextAreaField('Comments', [validators.Optional()])

    accept_tos = BooleanField('I accept the TOS')

test_server = Flask(__name__)

@test_server.route("/")
def index():
  return render_template("index.html")

@test_server.route("/link")
def link():
  return render_template("link.html")

# alternate_form route used for testing formaction
@test_server.route('/form', methods=['GET', 'POST'], endpoint="form")
@test_server.route('/alternate_form', methods=['GET', 'POST'])
def form_route():
  form = ContrivedForm(request.form)
  if request.method == 'POST' and form.validate():
    return render_template('submit.html', form=form)
  return render_template('form.html', form=form)

@test_server.route('/cookie')
def cookie():
  resp = make_response(render_template('cookie.html'))
  resp.set_cookie('examplecookie', 'examplevalue')
  return resp

if __name__ == "__main__":
    test_server.run(debug = True)
