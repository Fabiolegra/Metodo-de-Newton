"""
rotas
"""
from flask import flash, redirect, render_template, url_for

from graficos import app
from graficos.forms import Formulario
from graficos.funcoes import resultado_funcao


@app.route('/', methods=['GET', 'POST'])
def formulario():
    """
    Renderiza o formulário HTML e processa os dados submetidos.
    """
    # Cria uma instância do formulário
    form_ = Formulario()

    # Verifica se o formulário foi submetido e é válido
    if form_.validate_on_submit():
        try:
            # Tenta chamar a função resultado_funcao e redirecionar para a rota 'resultado'
            if resultado_funcao(form_):
                # Armazena o resultado em uma variável global e redireciona para a rota 'resultado'
                global graficoJson
                graficoJson = resultado_funcao(form_)
                return redirect(url_for('resultado'))
        except SyntaxError:
            # Se houver um erro de sintaxe, exibe uma mensagem de erro específica
            flash('Erro de sintaxe ao analisar a função.', 'alert-danger')
        except NameError:
            # Se houver um erro de nome, exibe uma mensagem de erro específica
            flash('Erro de nome ao analisar a função.', 'alert-danger')
        except Exception as e:
            # Se houver qualquer outro erro, exibe uma mensagem de erro genérica
            flash(f'Erro ao analisar a função', 'alert-danger')
            return redirect(url_for('padrao'))

    return render_template('formulario.html', form=form_)

@app.route('/resultado')
def resultado():
    """
    renderiza o grafico
    """
    return render_template('grafico.html', graficoJson=graficoJson)


@app.route('/informacao')
def informacao():
    """
    renderiza o grafico
    """
    return render_template('informacao.html')


@app.route('/padrao')
def padrao():
    """
    renderiza o grafico
    """
    return render_template('padrao.html')
