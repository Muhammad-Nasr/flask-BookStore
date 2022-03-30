from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length, Email
from main.models import Reader


class SearchForm(FlaskForm):
    search = StringField(label='Book', render_kw={'placeholder': 'search for you favourite book.'} )
    submit = SubmitField(label='Search')


class SaveForm(FlaskForm):
    book = HiddenField()
    save = SubmitField('Save')


class EditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField(label='Edit')

    def __init__(self, original_name, *args, **kwargs):
        super(EditForm,self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_username(self, username):
        if self.original_name != username.data:
            reader = Reader.query.filter_by(username=username.data).first()
            if reader:
                raise ValidationError('Please use a different username')




class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    message = TextAreaField('Message', validators=[
        DataRequired(), Length(min=0, max=200)])
    submit = SubmitField('Submit')