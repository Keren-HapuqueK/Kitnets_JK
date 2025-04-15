from django.shortcuts import render, redirect  # Importa funções para mostrar páginas e redirecionar
from django.db import connection  # Importa a conexão com o banco de dados
from django.http import HttpResponse, JsonResponse  # Importa respostas HTTP
from django.views.decorators.csrf import csrf_protect  # Importa proteção contra ataques CSRF
from .forms import LocadorForm  # Importa o formulário de Locador
import logging  # Importa o módulo de logging

logger = logging.getLogger(__name__)  # Configura o logger

def listar_locadores(request):  # Função para listar locadores
    search_query = request.GET.get('search', '').lower()  # Pega a busca do usuário e transforma em minúsculas
    ordenar_por = request.GET.get('ordenar_por', 'Nome')  # Pega o campo para ordenar, padrão é Nome
    with connection.cursor() as cursor:  # Abre a conexão com o banco de dados
        if search_query:  # Se tem busca
            cursor.execute(f"""
                SELECT ID_Locador, Nome, Telefone, RG, CPF_CNPJ, ID_Estado_Civil
                FROM Locador
                WHERE LOWER(Nome) LIKE %s
                ORDER BY {ordenar_por} ASC
            """, [f'%{search_query}%'])  # Busca locadores pelo nome
        else:  # Se não tem busca
            cursor.execute(f"""
                SELECT ID_Locador, Nome, Telefone, RG, CPF_CNPJ, ID_Estado_Civil
                FROM Locador
                ORDER BY {ordenar_por} ASC
            """)  # Busca todos os locadores
        locadores = cursor.fetchall()  # Pega todos os resultados
    return render(request, 'locadores/listar.html', {'locadores': locadores, 'search_query': search_query, 'ordenar_por': ordenar_por})  # Mostra a página com os locadores

def criar_locador(request):  # Função para criar locador
    if request.method == 'POST':  # Se o método é POST
        form = LocadorForm(request.POST)  # Pega os dados do formulário
        if form.is_valid():  # Se o formulário é válido
            data = form.cleaned_data  # Limpa os dados do formulário
            try:
                with connection.cursor() as cursor:  # Abre a conexão com o banco de dados
                    cursor.callproc('criar_locador', [
                        data['nome'],
                        data['telefone'],
                        data['rg'],
                        data['cpf_cnpj'],
                        data['estado_civil']
                    ])  # Chama o procedimento para criar locador
                    return redirect('listar_locadores')  # Redireciona para a listagem
            except Exception as e:  # Se tem erro
                return HttpResponse(f"Erro ao criar locador: {e}", status=500)  # Mostra o erro
    else:  # Se o método não é POST
        form = LocadorForm()  # Cria um formulário vazio
    return render(request, 'locadores/criar.html', {'form': form})  # Mostra a página para criar locador

def editar_locador(request, id_locador):  # Função para editar locador
    if request.method == 'POST':  # Se o método é POST
        form = LocadorForm(request.POST)  # Pega os dados do formulário
        if form.is_valid():  # Se o formulário é válido
            data = form.cleaned_data  # Limpa os dados do formulário
            try:
                with connection.cursor() as cursor:  # Abre a conexão com o banco de dados
                    cursor.callproc('editar_locador', [
                        id_locador,
                        data['nome'],
                        data['telefone'],
                        data['rg'],
                        data['cpf_cnpj'],
                        data['estado_civil']
                    ])  # Chama o procedimento para editar locador
                    return redirect('listar_locadores')  # Redireciona para a listagem
            except Exception as e:  # Se tem erro
                return HttpResponse(f"Erro ao editar locador: {e}", status=500)  # Mostra o erro
    else:  # Se o método não é POST
        locador = None  # Inicializa locador como None
        try:
            with connection.cursor() as cursor:  # Abre a conexão com o banco de dados
                cursor.execute("""
                    SELECT ID_Locador, Nome, Telefone, RG, CPF_CNPJ, ID_Estado_Civil
                    FROM Locador
                    WHERE ID_Locador = %s
                """, [id_locador])  # Busca o locador pelo ID
                locador = cursor.fetchone()  # Pega o locador
        except Exception as e:  # Se tem erro
            return HttpResponse(f"Erro ao carregar locador: {e}", status=500)  # Mostra o erro

        if locador is None:  # Se não encontrou o locador
            return HttpResponse("Locador não encontrado", status=404)  # Mostra mensagem de erro

        form = LocadorForm(initial={
            'nome': locador[1],
            'telefone': locador[2],
            'rg': locador[3],
            'cpf_cnpj': locador[4],
            'estado_civil': locador[5]
        })  # Preenche o formulário com os dados do locador
    return render(request, 'locadores/editar.html', {'form': form})  # Mostra a página para editar locador

@csrf_protect  # Protege contra ataques CSRF
def excluir_locador(request, id_locador):  # Função para excluir locador
    logger.debug(f"Tentando excluir o locador com ID: {id_locador}")  # Log de debug
    if request.method == "POST":  # Se o método é POST
        try:
            with connection.cursor() as cursor:  # Abre a conexão com o banco de dados
                cursor.callproc("excluir_locador", [id_locador])  # Chama o procedimento para excluir locador
            logger.debug(f"Locador com ID: {id_locador} excluído com sucesso")  # Log de sucesso
            return JsonResponse({"success": True})  # Retorna sucesso
        except Exception as e:  # Se tem erro
            logger.error(f"Erro ao excluir o locador com ID: {id_locador} - {str(e)}")  # Log de erro
            return JsonResponse({"success": False, "error": str(e)}, status=500)  # Retorna erro

    logger.error(f"Método inválido para excluir o locador com ID: {id_locador}")  # Log de método inválido
    return JsonResponse({"success": False, "error": "Método inválido"}, status=400)  # Retorna método inválido

def visualizar_locador(request, id_locador):  # Função para visualizar locador
    try:
        with connection.cursor() as cursor:  # Abre a conexão com o banco de dados
            cursor.execute("""
                SELECT l.ID_Locador, l.Nome, l.Telefone, l.RG, l.CPF_CNPJ, ec.Desc_Estado_Civil
                FROM Locador l
                LEFT JOIN Estado_Civil ec ON l.ID_Estado_Civil = ec.ID_Estado_Civil
                WHERE l.ID_Locador = %s
            """, [id_locador])  # Busca o locador pelo ID
            locador = cursor.fetchone()  # Pega o locador
            if locador is None:  # Se não encontrou o locador
                return HttpResponse("Locador não encontrado", status=404)  # Mostra mensagem de erro
            return render(request, 'locadores/visualizar.html', {'locador': locador})  # Mostra a página com os dados do locador
    except Exception as e:  # Se tem erro
        return HttpResponse(f"Erro ao visualizar locador: {e}", status=500)  # Mostra o erro