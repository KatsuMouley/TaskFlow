from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

from ..models import Task


class TaskForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired(), Length(min=2, max=120)])
    description = TextAreaField("Descrição", validators=[Length(max=2000)])
    status = SelectField("Status", choices=list(Task.STATUSES.items()), validators=[DataRequired()])
    assigned_to_id = SelectField("Responsável", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Salvar tarefa")
