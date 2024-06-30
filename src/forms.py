"""
Reune os formularios
"""
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired


class Formulario(FlaskForm):
    """
    Formulario que recebe a expressao e os palpites.

    Args:
        FlaskForm (class): herança para a criação de formulario.
    """

    funcao = StringField('Funcão:', validators=[DataRequired()])
    palpite1 = DecimalField('Palpite 1:', validators=[DataRequired()])
    palpite2 = DecimalField('Palpite 2:', validators=[DataRequired()])
    botao = SubmitField('Enviar')
