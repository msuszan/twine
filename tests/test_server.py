from flask import Flask, request, render_template
from wtforms import Form, validators
from wtforms import TextField, PasswordField, BooleanField, RadioField
from wtforms import SelectField, TextAreaField

class ContrivedForm(Form):
    name = TextField('Name')

    password = PasswordField('New Password')#, [
        #validators.EqualTo('confirm', message='Passwords must match')
    #])
    confirm = PasswordField('Repeat Password')

    gender = RadioField('Gender', choices=[('male','Male'),
        ('female','Female')], default='male')

    language_choices = [
        ('cpp', 'C++'),
        ('py', 'Python'),
        ('js', 'JavaScript')
    ]
    language = SelectField('Programming Language', choices=language_choices)

    comments = TextAreaField()

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

if __name__ == "__main__":
    test_server.run(debug = True)
