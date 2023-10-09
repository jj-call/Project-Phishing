from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField, SelectField, IntegerField, RadioField, DateTimeField, validators
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from my_app.models import User
from datetime import datetime


# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

  
class PreSimulationResponseForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, max=85)])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    training = SelectField('Training', choices=[('yes', 'Yes, I have been trained / had learning about it.'), ('no', 'No, I have never been trained / had any learning about it.')], validators=[DataRequired()])
    knowledge = SelectField('Knowledge', choices=[('yes', 'Yes, I do know what phishing is.'), ('no', 'No, I do not know what phishing is.')], validators=[DataRequired()])
    message = SelectField('Message', choices=[('yes', 'Yes, I have receieved a suspected phishing attempt.'), ('no', 'No, I have not receieved a suspected phishing attempt.')], validators=[DataRequired()])
    rating = RadioField('Rating', choices=[('1', 'Low confidence'), ('2', 'Developing confidence'), ('3', 'Fairly confident'), ('4', 'Strong confidence'), ('5', 'Very strong confidence')], validators=[DataRequired()])
    actions = SelectField('Actions', choices=[('option1', 'Open the email to check the content'), ('option2', 'Delete the email immediately'), ('option3', 'Report the email'), ('option4', 'Unsure')], validators=[DataRequired()])
    consequences = SelectField('Consequences', choices=[('option1', 'Yes fully understand'), ('option2', 'Partly understand'), ('option3', 'Do not fully understand')], validators=[DataRequired()])
    submit = SubmitField('Submit')

        
class PhishingSimulationForm(FlaskForm):
    challenge_id = StringField('Challenge ID', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', default=datetime.now, format='%Y-%m-%d %H:%M:%S')
    # Checkbox for phishing identification
    phishing = SelectField('Is this a genuine or a phishing email?', 
                           choices=[('', 'Choose...'), ('genuine', 'Genuine'), ('phishing', 'Phishing'), ('unsure', 'Unsure')],
                           validators=[validators.DataRequired(message="Please identify the email.")])

    # Dropdown for confidence level
    confidence = SelectField('Confidence', 
                             choices=[('', 'Choose...'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
                             validators=[validators.DataRequired(message="Please select a confidence level.")])

    # TextArea for reasoning
    reason = TextAreaField('Reason', [validators.Optional()])
    
    # Hidden field for clicked link
    clicked_link = HiddenField(default="False")
    
    # Hidden field for start time
    start_time = HiddenField(validators=[validators.DataRequired(message="Please start the simulation.")])
    
    # Submit button
    submit = SubmitField('Submit')
    
    
class PostSimulationForm(FlaskForm):
    awareness = SelectField('Awareness', choices=[('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
    ratings = RadioField('Ratings', choices=[('1', 'Low Confidence'), ('2', 'Developing Confidence'), ('3', 'Fairly Confident'), ('4', 'Strong Confidence'), ('5', 'Very Strong Confidence')], validators=[DataRequired()])
    helpful = SelectField('Helpful', choices=[('option1', 'Identifying potential phishing emails'), ('option2', 'Handling and managing the emails'), ('option3', 'Realising potential consequences'), ('option4', 'It was not that helpful')], validators=[DataRequired()])
    act = SelectField('Act', choices=[('option1', 'Open the email to check the content'), ('option2', 'Delete the email immediately'), ('option3', 'Report the email')], validators=[DataRequired()])
    behaviour = SelectField('Behaviour', choices=[('option1', 'Yes, I will be more attentive to what I click on or view.'), ('option2', 'Perhaps, sometimes I will try to be more attentive and cautious.'), ('option3', 'No, I will continue my normal behaviours; the simulation had no influence.')], validators=[DataRequired()])
    effective = RadioField('Effective', choices=[('1', 'Not effective at all'), ('2', 'Somewhat effective'), ('3', 'Moderately effective'), ('4', 'Very effective'), ('5', 'Extremely effective')], validators=[DataRequired()])
    life = SelectField('Life', choices=[('option1', 'Yes'), ('option2', 'No')], validators=[DataRequired()])
    recommend = SelectField('Recommend', choices=[('option1', 'Yes'), ('option2', 'No')], validators=[DataRequired()])
    submit = SubmitField('Submit')

