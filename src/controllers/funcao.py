import sympy as sp

from .verificacao import Verificacao


class Funcao:
    def __init__(self) -> None:
        self.funcao = None

    def criar_funcao(self, expressao: str) -> callable:
        """
        Cria uma função a partir de uma expressão matemática.

        Args:
            expressao (str): A expressão matemática como uma string.

        Returns:
            function: A função correspondente à expressão.
        """
        x = sp.symbols('x')
        f = sp.sympify(expressao)
        self.funcao = sp.lambdify(x, f)
        return self.funcao

    def derivada(self, x: float, h: float = 1e-6) -> float:
        """
        Calcula a derivada numérica de uma função.

        Args:
            funcao (function): A função para a qual calcular a derivada.
            x (float): O ponto no qual calcular a derivada.
            h (float): O tamanho do passo para calcular a derivada.

        Returns:
            float: O valor da derivada da função em x.
        """
        return (self.funcao(x + h) - self.funcao(x - h)) / (2 * h)

    def metodo_newton_raphson(
        self, x0: float, epsilon: float = 1e-4, kmax: int = 1000
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
        while abs(self.funcao(x)) > epsilon and k < kmax:
            try:
                x = x - self.funcao(x) / self.derivada(x)
            except ZeroDivisionError:
                x = 0
                break
            else:
                iteracoes.append(x)
                k += 1
        x = Verificacao.check_aproximacao(x, self.funcao)
        return x.real, self.funcao(x.real), iteracoes
