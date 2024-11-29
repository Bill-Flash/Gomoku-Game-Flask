
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, widgets, RadioField, FileField, TextAreaField
from wtforms.validators import data_required, ValidationError, DataRequired, Email, EqualTo, InputRequired, Regexp


# inspired from https://wtforms.readthedocs.io/en/2.3.x/validators/#wtforms.validators
class Length(object):
    # the default max = 20 and min = 4
    def __init__(self, min=4, max=20, message=None, label=None):
        self.min = min
        self.max = max
        if not label:
            label = ""
        self.label = label
        if not message:
            message = u'{} must be between %i and %i characters long.'.format(label) % (min, max)
        self.message = message

    def __call__(self, form, field):
        l = len(field.data)
        if (self.min > l) or (l > self.max):
            raise ValidationError(self.message)

# check the allowed type
class FileAllowed(object):
    def __init__(self, message=None, label=None):
        if not label:
            label = "File"
        self.label = label
        if not message:
            message = "Not a valid file tpye!"
        self.message = message

    def __call__(self, form, field):
        file = field.data
        if file is None:
            raise ValidationError(self.message)
        fileType = file.headers['Content-Type']

        # 2 types is allowed
        ALLOWED_TYPE = ['image/jpeg','image/png']
        if not fileType in ALLOWED_TYPE:
            raise ValidationError(self.message)

# Login form used in logon.html
class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired('Please enter the username or email')])
    password = PasswordField('Password', validators=[DataRequired('Please enter the password')])
    submit = SubmitField('Sign in')

# Signup for register.html
class SignUpForm(FlaskForm):
    # username should be between 4-15 characters long, and starts with letter,
        # and only consists of letters, digits, and underscores (_).
    # Password should be between 5-16 characters, can contain
        # letters, digits, and special characters. 5-15 characters allowed.
    username = StringField('Username', validators=[DataRequired(), Length(max=16, label=u'Username'),
                                                   Regexp(regex="^[a-zA-Z][a-zA-Z0-9_]{3,14}$", message=u"Not a valid username.")],
                           render_kw={'placeholder': 'Your username',
                                      'title':'Please start with letter.(4-15 characters)'},
                           widget=widgets.TextInput())
    password = PasswordField('Password', validators=[InputRequired(message=u'Enter your password.'),
                                                     Regexp(regex="^(?!(?:[^a-zA-Z]|\D|[a-zA-Z0-9])$).{5,15}$",
                                                            message=u"Not a valid password.")],
                             render_kw={'title': 'Please contain letters, digits, or special characters.(5-15 characters)'})
    confirm = PasswordField('Confirm', validators=[EqualTo('password', u'You should enter two of the same passwords.')],
                            render_kw={'placeholder': 'Repeat password', 'title': 'Repeat password'})
    emailA = StringField('Email Address', validators=[Email(u'Enter a correct format of Email Address.'),
                                                      DataRequired(u"Please fill out your Email Address.")],
                         render_kw={'placeholder': u'someone@somedomain.com',
                                    'title':'Please provide a valid email.'})
    submit = SubmitField('Register')

# RankSearch for search.html and rank.html
class RankSearchForm(FlaskForm):
    search = StringField('Search by Username', validators=[DataRequired()])
    submit = SubmitField('Search')

# Personal Information: Divide them into two parts (Profile, Avatar)
class ProfileForm(FlaskForm):
    gender = RadioField('Gender', choices=[u'Male',u'Female',u'Unknown'],
                        validators=[DataRequired()],
                        render_kw={'title':'Your Introduction.'},default=[u'Unknown'])
    #No need for requierd
    intro = TextAreaField('Introduction',render_kw={'title':'Your Introduction.', 'rows':'10', 'cols':'40'})
    submit = SubmitField('Upload Personal Information')

class AvatarForm(FlaskForm):
    photo = FileField('Avatar', validators=[FileAllowed()])
    submit = SubmitField('Update Avatar')