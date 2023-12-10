from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, ValidationError, Regexp, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[
        DataRequired(),
        Regexp('^[a-zA-Z]+\\.[a-zA-Z]+[0-9]+$', message="Username must be in the format 'firstname.lastname' or 'firstname.lastname123'")])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address.'),
        Regexp('^[a-zA-Z]+\\.[a-zA-Z]+[0-9]+@corn\\.com$', message="Email must be in the format 'firstname.lastname@corn.com'")])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long."),
        Regexp('^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$', message="Password must include a number, an uppercase and a lowercase letter.")])
    dept = RadioField('Department', choices=[('HR', 'HR'), ('Marketing', 'Marketing'), ('R&D', 'R&D'), ('Development', 'Development'), ('IT', 'IT')], validators=[DataRequired()])
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


class EditUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[
        DataRequired(),
        Regexp('^[a-zA-Z]+\\.[a-zA-Z]+$', message="Username must be in the format 'firstname.lastname'")])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address.'),
        Regexp('^[a-zA-Z]+\\.[a-zA-Z]+@corn\\.com$', message="Email must be in the format 'firstname.lastname@corn.com'")])
    dept = RadioField('Department', choices=[('HR', 'HR'), ('Marketing', 'Marketing'), ('R&D', 'R&D'), ('Development', 'Development'), ('IT', 'IT')], validators=[DataRequired()])
    
    # Role field is only included if the current user is an admin
    role = RadioField('Role', choices=[('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()], default='user')

    submit = SubmitField('Update')

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        # If the current user is not an admin, remove the role field
        if not (current_user.is_authenticated and current_user.role == 'admin'):
            del self.role