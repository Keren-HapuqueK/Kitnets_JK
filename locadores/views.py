from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from .forms import LocadorForm
import logging

logger = logging.getLogger(__name__)

def listar_locadores(request):
    search_query = request.GET.get('search', '').lower()
    ordenar_por = request.GET.get('ordenar_por', 'Nome')  # Ordena por Nome por padrão
    with connection.cursor() as cursor:
        if search_query:
            cursor.execute(f"""
                SELECT ID_Locador, Nome, Telefone, RG, CPF_CNPJ, ID_Estado_Civil
                FROM Locador
                WHERE LOWER(Nome) LIKE %s
                ORDER BY {ordenar_por} ASC
            """, [f'%{search_query}%'])
        else:
            cursor.execute(f"""
                SELECT ID_Locador, Nome, Telefone, RG, CPF_CNPJ, ID_Estado_Civil
                FROM Locador
                ORDER BY {ordenar_por} ASC
            """)
        locadores = cursor.fetchall()
    return render(request, 'locadores/listar.html', {'locadores': locadores, 'search_query': search_query, 'ordenar_por': ordenar_por})

def criar_locador(request):
    if request.method == 'POST':
        form = LocadorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('criar_locador', [
                        data['nome'],
                        data['telefone'],
                        data['rg'],
                        data['cpf_cnpj'],
                        data['estado_civil']
                    ])
                    return redirect('listar_locadores')  # Redireciona para a listagem
            except Exception as e:
                return HttpResponse(f"Erro ao criar locador: {e}", status=500)
    else:
        form = LocadorForm()
    return render(request, 'locadores/criar.html', {'form': form})

def editar_locador(request, id_locador):
    if request.method == 'POST':
        form = LocadorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('editar_locador', [
                        id_locador,
                        data['nome'],
                        data['telefone'],
                        data['rg'],
                        data['cpf_cnpj'],
                        data['estado_civil']
                    ])
                    return redirect('listar_locadores')  # Redireciona para a listagem
            except Exception as e:
                return HttpResponse(f"Erro ao editar locador: {e}", status=500)
    else:
        locador = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Locador WHERE ID_Locador = %s", [id_locador])
                locador = cursor.fetchone()
        except Exception as e:
            return HttpResponse(f"Erro ao carregar locador: {e}", status=500)

        if locador is None:
            return HttpResponse("Locador não encontrado", status=404)

        form = LocadorForm(initial={
            'nome': locador[1],
            'telefone': locador[2],
            'rg': locador[3],
            'cpf_cnpj': locador[4],
            'estado_civil': locador[5]
        })
    return render(request, 'locadores/editar.html', {'form': form})

def excluir_locador(request, id_locador):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('excluir_locador', [id_locador])
                return redirect('listar_locadores')  # Redireciona para a listagem
        except Exception as e:
            return HttpResponse(f"Erro ao excluir locador: {e}", status=500)
    else:
        locador = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Locador WHERE ID_Locador = %s", [id_locador])
                locador = cursor.fetchone()
        except Exception as e:
            return HttpResponse(f"Erro ao carregar locador: {e}", status=500)

        if locador is None:
            return HttpResponse("Locador não encontrado", status=404)

        return render(request, 'locadores/excluir.html', {'locador': locador})
