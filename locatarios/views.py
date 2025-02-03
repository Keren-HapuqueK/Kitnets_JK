from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from .forms import LocatarioForm
import logging

logger = logging.getLogger(__name__)

def listar_locatarios(request):
    search_query = request.GET.get('search', '').lower()
    with connection.cursor() as cursor:
        if search_query:
            cursor.execute("""
                SELECT l.ID_Locatario, l.Nome, l.Telefone, l.RG, l.CPF_CNPJ, ec.Desc_Estado_Civil
                FROM Locatario l
                LEFT JOIN Estado_Civil ec ON l.ID_Estado_Civil = ec.ID_Estado_Civil
                WHERE LOWER(l.Nome) LIKE %s
                ORDER BY l.Nome
            """, [f'%{search_query}%'])
        else:
            cursor.execute("""
                SELECT l.ID_Locatario, l.Nome, l.Telefone, l.RG, l.CPF_CNPJ, ec.Desc_Estado_Civil
                FROM Locatario l
                LEFT JOIN Estado_Civil ec ON l.ID_Estado_Civil = ec.ID_Estado_Civil
                ORDER BY l.Nome
            """)
        locatarios = cursor.fetchall()
    return render(request, 'locatarios/listar.html', {'locatarios': locatarios, 'search_query': search_query})

def criar_locatario(request):
    if request.method == 'POST':
        form = LocatarioForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('criar_locatario', [
                        data['nome'],
                        data['telefone'],
                        data['rg'],
                        data['cpf_cnpj'],
                        data['estado_civil']
                    ])
                    return redirect('listar_locatarios')  # Redireciona para a listagem
            except Exception as e:
                return HttpResponse(f"Erro ao criar locatário: {e}", status=500)
    else:
        form = LocatarioForm()
    return render(request, 'locatarios/criar.html', {'form': form})

def editar_locatario(request, id_locatario):
    if request.method == 'POST':
        form = LocatarioForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('editar_locatario', [
                        id_locatario,
                        data['nome'],
                        data['telefone'],
                        data['rg'],
                        data['cpf_cnpj'],
                        data['estado_civil']
                    ])
                    return redirect('listar_locatarios')  # Redireciona para a listagem
            except Exception as e:
                return HttpResponse(f"Erro ao editar locatário: {e}", status=500)
    else:
        locatario = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Locatario WHERE ID_Locatario = %s", [id_locatario])
                locatario = cursor.fetchone()
        except Exception as e:
            return HttpResponse(f"Erro ao carregar locatário: {e}", status=500)

        if locatario is None:
            return HttpResponse("Locatário não encontrado", status=404)

        form = LocatarioForm(initial={
            'nome': locatario[1],
            'telefone': locatario[2],
            'rg': locatario[3],
            'cpf_cnpj': locatario[4],
            'estado_civil': locatario[5]
        })
    return render(request, 'locatarios/editar.html', {'form': form})

def excluir_locatario(request, id_locatario):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('excluir_locatario', [id_locatario])
                return redirect('listar_locatarios')  # Redireciona para a listagem
        except Exception as e:
            return HttpResponse(f"Erro ao excluir locatário: {e}", status=500)
    else:
        locatario = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Locatario WHERE ID_Locatario = %s", [id_locatario])
                locatario = cursor.fetchone()
        except Exception as e:
            return HttpResponse(f"Erro ao carregar locatário: {e}", status=500)

        if locatario is None:
            return HttpResponse("Locatário não encontrado", status=404)

        return render(request, 'locatarios/excluir.html', {'locatario': locatario})
