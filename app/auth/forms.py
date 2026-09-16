from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(min=2, max=80)])
    email = EmailField("E-mail", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=128)])
    confirm_password = PasswordField(
        "Confirmar senha", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Criar conta")


class LoginForm(FlaskForm):
    email = EmailField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")
