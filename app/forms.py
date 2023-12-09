from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, ValidationError
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email')
    password = PasswordField('Password', validators=[DataRequired()])
    role = RadioField(choices=[(0, 'Customer'), (1, 'Staff'), (2, 'Admin')], default=0, validators=[DataRequired()])
    dept = RadioField(choices=[(1, 'HR'), (2, 'Marketing'), (3, 'R&D'), (4, 'Development')], default=0,
                      validators=[DataRequired()])
    submit = SubmitField('Register')


class TicketForm(FlaskForm):

    created_by = StringField('Created by', validators=[DataRequired()])
    dept = SelectField('Department', choices=[
        ('1', 'HR'),
        ('2', 'Marketing'),
        ('3', 'R&D'),
        ('4', 'Development')
    ], validators=[DataRequired()])
    title = StringField('Title: ', validators=[DataRequired()])
    assigned_to = StringField('Assigned To', default='admin')   # Default to admin
    status = SelectField(choices=[('open', 'Open'), ('in-progress', 'In-Progress'), ('closed', 'Closed')])
    priority = SelectField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    description = StringField('Description')
    location = SelectField('Location', choices=[
        ('office1', 'Office 1'),
        ('office2', 'Office 2'),
        ('office3', 'Office 3')
    ])
    attachment = StringField('Attachment(s)')
    submit = SubmitField('Submit Ticket')
