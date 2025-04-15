from django.shortcuts import render, redirect  # Importa funções para mostrar páginas e redirecionar
from django.http import HttpResponse, JsonResponse  # Importa funções para enviar respostas HTTP
from django.db import connection  # Importa a conexão com o banco de dados
from .forms import FormaPagamentoForm  # Importa o formulário de pagamento
import logging  # Importa o módulo de registro de logs
from django.views.decorators.csrf import csrf_protect  # Importa proteção contra CSRF

logger = logging.getLogger(__name__)  # Cria um registrador de logs

def executar_sql(query, params=None, fetch_one=False):  # Define uma função para executar comandos SQL
    try:
        with connection.cursor() as cursor:  # Abre uma conexão com o banco de dados
            cursor.execute(query, params)  # Executa o comando SQL
            if query.strip().lower().startswith("select"):  # Verifica se é um comando SELECT
                return cursor.fetchone() if fetch_one else cursor.fetchall()  # Retorna um ou todos os resultados
    except Exception as e:  # Se ocorrer um erro
        logger.error(f"Erro ao executar SQL: {e}")  # Registra o erro
        raise  # Lança o erro novamente

def listar_formas_pagamento(request):  # Define uma função para listar formas de pagamento
    search_query = request.GET.get('search', '').lower()  # Pega o termo de busca da URL
    ordenar_por = request.GET.get('ordenar_por', 'Desc_Forma_Pgto')  # Pega o campo de ordenação da URL
    with connection.cursor() as cursor:  # Abre uma conexão com o banco de dados
        if search_query:  # Se houver um termo de busca
            cursor.execute(f"""
                SELECT * FROM Forma_Pagamento
                WHERE LOWER(Desc_Forma_Pgto) LIKE %s
                ORDER BY {ordenar_por} ASC
            """, [f'%{search_query}%'])  # Executa a busca no banco de dados
        else:
            cursor.execute(f"SELECT * FROM Forma_Pagamento ORDER BY {ordenar_por} ASC")  # Executa a busca sem filtro
        formas_pagamento = cursor.fetchall()  # Pega todos os resultados
    return render(request, 'forma_pagamento/listar.html', {'formas_pagamento': formas_pagamento, 'search_query': search_query, 'ordenar_por': ordenar_por})  # Mostra a página com os resultados

def criar_forma_pagamento(request):  # Define uma função para criar uma nova forma de pagamento
    if request.method == 'POST':  # Se o método da requisição for POST
        form = FormaPagamentoForm(request.POST)  # Cria um formulário com os dados enviados
        if form.is_valid():  # Se o formulário for válido
            desc_forma_pgto = form.cleaned_data['desc_forma_pgto']  # Pega o valor do campo de descrição
            try:
                with connection.cursor() as cursor:  # Abre uma conexão com o banco de dados
                    cursor.callproc('criar_forma_pagamento', [desc_forma_pgto])  # Chama o procedimento para criar a forma de pagamento
                    return redirect('listar_formas_pagamento')  # Redireciona para a lista de formas de pagamento
            except Exception as e:  # Se ocorrer um erro
                return HttpResponse(f"Erro ao adicionar forma de pagamento: {e}", status=500)  # Retorna uma resposta de erro
    else:
        form = FormaPagamentoForm()  # Cria um formulário vazio
    return render(request, 'forma_pagamento/criar.html', {'form': form})  # Mostra a página com o formulário

def editar_forma_pagamento(request, id_forma_pagamento):  # Define uma função para editar uma forma de pagamento
    if request.method == 'POST':  # Se o método da requisição for POST
        form = FormaPagamentoForm(request.POST)  # Cria um formulário com os dados enviados
        if form.is_valid():  # Se o formulário for válido
            desc_forma_pgto = form.cleaned_data['desc_forma_pgto']  # Pega o valor do campo de descrição
            try:
                with connection.cursor() as cursor:  # Abre uma conexão com o banco de dados
                    cursor.callproc('editar_forma_pagamento', [id_forma_pagamento, desc_forma_pgto])  # Chama o procedimento para editar a forma de pagamento
                    return redirect('listar_formas_pagamento')  # Redireciona para a lista de formas de pagamento
            except Exception as e:  # Se ocorrer um erro
                return HttpResponse(f"Erro ao editar forma de pagamento: {e}", status=500)  # Retorna uma resposta de erro
    else:
        forma_pagamento = None  # Inicializa a variável da forma de pagamento
        try:
            with connection.cursor() as cursor:  # Abre uma conexão com o banco de dados
                cursor.execute("SELECT * FROM Forma_Pagamento WHERE ID_Forma_Pagamento = %s", [id_forma_pagamento])  # Executa a busca da forma de pagamento
                forma_pagamento = cursor.fetchone()  # Pega o resultado
        except Exception as e:  # Se ocorrer um erro
            return HttpResponse(f"Erro ao carregar forma de pagamento: {e}", status=500)  # Retorna uma resposta de erro

        if forma_pagamento is None:  # Se a forma de pagamento não for encontrada
            return HttpResponse("Forma de pagamento não encontrada", status=404)  # Retorna uma resposta de não encontrado

        form = FormaPagamentoForm(initial={'desc_forma_pgto': forma_pagamento[1]})  # Cria um formulário com os dados da forma de pagamento
    return render(request, 'forma_pagamento/editar.html', {'form': form})  # Mostra a página com o formulário

def excluir_forma_pagamento(request, id_forma_pagamento):  # Define uma função para excluir uma forma de pagamento
    if request.method == 'POST':  # Se o método da requisição for POST
        try:
            with connection.cursor() as cursor:  # Abre uma conexão com o banco de dados
                cursor.callproc('excluir_forma_pagamento', [id_forma_pagamento])  # Chama o procedimento para excluir a forma de pagamento
                return JsonResponse({'success': True})  # Retorna uma resposta de sucesso
        except Exception as e:  # Se ocorrer um erro
            return JsonResponse({'success': False, 'error': str(e)}, status=500)  # Retorna uma resposta de erro
    else:
        forma_pagamento = None  # Inicializa a variável da forma de pagamento
        try:
            with connection.cursor() as cursor:  # Abre uma conexão com o banco de dados
                cursor.execute("SELECT * FROM Forma_Pagamento WHERE ID_Forma_Pagamento = %s", [id_forma_pagamento])  # Executa a busca da forma de pagamento
                forma_pagamento = cursor.fetchone()  # Pega o resultado
        except Exception as e:  # Se ocorrer um erro
            return HttpResponse(f"Erro ao carregar forma de pagamento: {e}", status=500)  # Retorna uma resposta de erro

        if forma_pagamento is None:  # Se a forma de pagamento não for encontrada
            return HttpResponse("Forma de pagamento não encontrada", status=404)  # Retorna uma resposta de não encontrado

        return render(request, 'forma_pagamento/excluir.html', {'forma_pagamento': forma_pagamento})  # Mostra a página de confirmação de exclusão