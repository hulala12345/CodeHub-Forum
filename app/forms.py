from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class QuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    tags = StringField('Tags (comma separated)')
    submit = SubmitField('Post')

class AnswerForm(FlaskForm):
    body = TextAreaField('Your Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')
