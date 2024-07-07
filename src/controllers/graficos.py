import plotly
import plotly.graph_objects as go
import json
import numpy as np
from .verificacao import Verificacao


class Grafico:
    @staticmethod
    def plotar_funcao(
        valores_x: list, funcao: callable, expressao: str
    ) -> go.Scatter:
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

    @staticmethod
    def plotar_raizes(raiz: float, fdex: float, color: str) -> go.Scatter:
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
            name=f'{Verificacao.is_raiz(fdex)} = {raiz}',
            marker={'color': color, 'size': 10},
        )
        return ponto

    @staticmethod
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
        intervalo_x = np.linspace(
            intervalo_x[0] - 10, intervalo_x[1] + 10, 100
        )
        if Verificacao.raiz_existe(funcao, intervalo_x):
            funcao_linha = Grafico.plotar_funcao(
                intervalo_x, funcao, expressao
            )
            ponto1 = Grafico.plotar_raizes(
                raiz=raiz1[0], fdex=raiz1[1], color='red'
            )
            ponto2 = Grafico.plotar_raizes(
                raiz=raiz2[0], fdex=raiz2[1], color='yellow'
            )
            fig = go.Figure(data=[funcao_linha, ponto1, ponto2], layout=layout)
        else:
            funcao_linha = Grafico.plotar_funcao(
                intervalo_x, funcao, 'NÃO EXISTEM RAIZES'
            )
            fig = go.Figure(data=[funcao_linha], layout=layout)
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
