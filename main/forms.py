from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, PasswordField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Email



class SearchForm(FlaskForm):
    search = StringField(label='Book', render_kw={'placeholder': 'search by book name, author, category.'} )
    submit = SubmitField(label='Done')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class SaveForm(FlaskForm):
    book = HiddenField()
    save = SubmitField('Save')

## create forms for add.html
class Form_add(FlaskForm):
    title= StringField(label='Movie Title')
    submit= SubmitField(label='Add Movie')