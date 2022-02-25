from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sqlalchemy import text
from application import engine


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=4, max=20)])

    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm_Password", validators=[
                                     DataRequired(), EqualTo('password')])

    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = engine.execute(text("""SELECT * FROM Users WHERE User_Name='{username.data}' """)
        ).fetchone()
        # result = engine.execute(user).fetchone()
        # print(result)
        if user:
            # print(1/0)
            raise ValidationError("That user name taken")
            

    def validate_email(self, email):
        email = engine.execute(text("""SELECT * FROM Users WHERE Email='{email.data}' """)
        ).fetchone()
        # result = engine.execute(email).fetchone()
        # print(result)

        if email:
            # print(1/0)
            raise ValidationError("That email is in the database")
            # print('error')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])

    # email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])
    # confirm_Password = PasswordField('Confirm_Password', validators=[DataRequired(), EqualTo('password')])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
