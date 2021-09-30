from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired,Length,Optional

class UserAddForm(FlaskForm):
    """Form for adding user"""
    
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=6)])
    

class LoginForm(FlaskForm):
    """Form for logging in"""

    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])


class SearchForm(FlaskForm):
    """Search for a cocktail by name"""

    drink_name = StringField("Search",validators=[Optional()])
