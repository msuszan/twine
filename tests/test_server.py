from flask import Flask, request, render_template
from wtforms import Form, validators
from wtforms import TextField, PasswordField, BooleanField, RadioField
from wtforms import SelectField, TextAreaField

class ContrivedForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=25)])

    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    gender = RadioField('Gender', choices=[('male','Male'),
        ('female','Female')])

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

@test_server.route('/form', methods=['GET', 'POST'])
def register():
  form = ContrivedForm(request.form)
  if request.method == 'POST' and form.validate():
    return render_template('submit.html', form=form)
  return render_template('form.html', form=form)

if __name__ == "__main__":
    test_server.run(debug = True)
