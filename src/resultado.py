"""
Reune todas as funcoes
"""
from wtforms.form import Form
from .controllers.graficos import Grafico
from .controllers.funcao import Funcao


def resultado_funcao(formulario: Form) -> bool:
    """
    Calcula e plota o gráfico de uma função usando o método de Newton-Raphson.

    Args:
        formulario: Um objeto contendo os dados do formulário.

    Returns:
        bool: True se a função foi plotada com sucesso, False se houve um erro na entrada.
    """
    if not 'x' in formulario.funcao.data.lower():
        return False
    try:
        expressao = formulario.funcao.data.lower()
        instancia_funcao = Funcao()
        funcao = instancia_funcao.criar_funcao(expressao)
        x1, y1, _ = instancia_funcao.metodo_newton_raphson(
            float(formulario.palpite1.data)
        )
        x2, y2, _ = instancia_funcao.metodo_newton_raphson(
            float(formulario.palpite2.data)
        )
    except (SyntaxError, NameError, UnboundLocalError):
        return False
    return Grafico.plotar_grafico(
        funcao, [x1, y1], [x2, y2], expressao, intervalo_x=sorted([x1, x2])
    )
