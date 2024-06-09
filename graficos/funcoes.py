"""
Reune todas as funcoes
"""
import json

import numpy as np
import plotly
import plotly.graph_objects as go
import sympy as sp
from wtforms.form import Form


def criar_funcao(expressao: str) -> callable:
    """
    Cria uma função a partir de uma expressão matemática.

    Args:
        expressao (str): A expressão matemática como uma string.

    Returns:
        function: A função correspondente à expressão.
    """
    x = sp.symbols('x')
    f = sp.sympify(expressao)
    return sp.lambdify(x, f)


def resultado_funcao(formulario: Form) -> bool:
    """
    Calcula e plota o gráfico de uma função usando o método de Newton-Raphson.

    Args:
        formulario: Um objeto contendo os dados do formulário.

    Returns:
        bool: True se a função foi plotada com sucesso, False se houve um erro na entrada.
    """
    if not 'x' in formulario.funcao.data:
        return False
    try:
        expressao = formulario.funcao.data
        funcao = criar_funcao(expressao)
        x1, y1, _ = metodo_newton_raphson(
            funcao, float(formulario.palpite1.data)
        )
        x2, y2, _ = metodo_newton_raphson(
            funcao, float(formulario.palpite2.data)
        )
    except (SyntaxError, NameError, UnboundLocalError):
        return False
    return plotar_grafico(
        funcao, [x1, y1], [x2, y2], expressao, intervalo_x=sorted([x1, x2])
        )


def metodo_newton_raphson(
    funcao: callable, x0: float, epsilon: float = 1e-4, kmax: int = 1000
) -> tuple:
    """
    Aplica o método de Newton-Raphson para encontrar uma raiz de uma função.

    Args:
        funcao (function): A função para a qual encontrar a raiz.
        x0 (float): O palpite inicial para a raiz.
        epsilon (float): A tolerância para a convergência.
        kmax (int): O número máximo de iterações.

    Returns:
        tuple: a raiz encontrada, o valor da função na raiz e a lista de iterações.
    """
    x = x0
    k = 0
    iteracoes = []
    while abs(funcao(x)) > epsilon and k < kmax:
        try:
            x = x - funcao(x) / derivada(funcao, x)
        except ZeroDivisionError:
            x = 0
            break
        else:
            iteracoes.append(x)
            k += 1
    x = check_aproximacao(x, funcao)
    return x.real, funcao(x.real), iteracoes


def derivada(funcao: callable, x: float, h: float = 1e-6) -> float:
    """
    Calcula a derivada numérica de uma função.

    Args:
        funcao (function): A função para a qual calcular a derivada.
        x (float): O ponto no qual calcular a derivada.
        h (float): O tamanho do passo para calcular a derivada.

    Returns:
        float: O valor da derivada da função em x.
    """
    return (funcao(x + h) - funcao(x - h)) / (2 * h)


def check_aproximacao(x: float, funcao: callable) -> float:
    """
    checa se a aproximação é a raiz.

    Args:
        funcao (function): A função para a qual calcular a expressao matematica.
        x (float): O ponto no qual calcular a derivada.

    Returns:
        float: O valor de x.
    """
    if funcao(round(x.real)) == 0:
        return round(x.real)
    return x


def israiz(y: str) -> str:
    """
    Verifica se um número é uma raiz.

    Args:
        y (str): O número a ser verificado.
    Returns:
        str: Uma mensagem indicando se y é uma raiz ou não.
    """
    if y == 0:
        return 'É RAIZ'
    return 'É UMA APROXIMAÇÃO'

def raiz_existe(funcao: callable, valores_x: list) -> bool:
    """
    Verifica se uma raiz existe.

    Args:
        funcao (callable): Função matemática.
        valores_x (list): Valores de x.

    Returns:
        bool: True se uma raiz existe, False caso contrário.
    """
    # Calcula os valores de y para cada valor de x
    valores_y = [y for y in funcao(valores_x)]
    # Verifica se há uma mudança de sinal nos valores de y
    if (
        funcao(0) == 0
    ):
        return True
    min_y, max_y = min(valores_y), max(valores_y)
    # Se o produto for negativo ou zero, implica que há uma raiz
    if min_y * max_y <= 0:
        return True
    return False


def plotar_funcao(valores_x: list, funcao: callable, expressao: str) -> go.Scatter:
    """Plota uma função.

        Args:
            valores_x (list): Lista de valores para o eixo x.
            funcao (callable): Função a ser plotada.
            expressao (str): Expressão da função.

        Returns:
            go.Scatter: Objeto Scatter do Plotly.
    """
    funcao_linha = go.Scatter(
        x=valores_x,
        y=funcao(valores_x),
        mode='lines',
        name=expressao,
    )
    return funcao_linha


def plotar_raizes(raiz:float, fdex:float, color: str) -> go.Scatter:
    """
    Plota um ponto dado x,y no grafico.

    Args:
        x (float): raiz
        y (float): valor de f(x)
        color (str): cor do ponto

    Returns:
        go.Scatter: um ponto para a criação do grafico.
    """
    ponto = go.Scatter(
        x=[raiz],
        y=[fdex],
        mode='markers',
        name=f'{israiz(fdex)} = {raiz}',
        marker={'color': color, 'size': 10},
    )
    return ponto


def plotar_grafico(
    funcao: callable,
    raiz1: list,
    raiz2: list,
    expressao: str,
    intervalo_x: float,
) -> str:
    """
    Plota um gráfico de uma função com as raízes indicadas.

    Args:
        funcao (function): A função a ser plotada.
        x1 (float): A coordenada x da primeira raiz.
        y1 (float): A coordenada y da primeira raiz.
        x2 (float): A coordenada x da segunda raiz.
        y2 (float): A coordenada y da segunda raiz.
        expressao (str): A expressão matemática correspondente à função.

    Returns:
        str: Uma representação JSON do gráfico Plotly.
    """
    layout = go.Layout(
        title='Método de Newton-Raphson',
        xaxis={'title': 'eixo X'},
        yaxis={'title': 'eixo Y'},
    )
    intervalo_x = np.linspace(intervalo_x[0] - 10, intervalo_x[1] + 10, 100)
    if raiz_existe(funcao, intervalo_x):
        funcao_linha = plotar_funcao(intervalo_x, funcao, expressao)
        ponto1 = plotar_raizes(
            raiz=raiz1[0], fdex=raiz1[1], color='red'
        )
        ponto2 = plotar_raizes(
            raiz=raiz2[0], fdex=raiz2[1], color='yellow'
        )
        fig = go.Figure(data=[funcao_linha, ponto1, ponto2], layout=layout)
    else:
        funcao_linha = plotar_funcao(intervalo_x, funcao, 'NÃO EXISTEM RAIZES')
        fig = go.Figure(data=[funcao_linha], layout=layout)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
