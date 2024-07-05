class Verificacao:
    @staticmethod
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

    @staticmethod
    def is_raiz(y: str) -> str:
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

    @staticmethod
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
        if funcao(0) == 0:
            return True
        min_y, max_y = min(valores_y), max(valores_y)
        # Se o produto for negativo ou zero, implica que há uma raiz
        if min_y * max_y <= 0:
            return True
        return False
