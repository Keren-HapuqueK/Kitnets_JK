from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse, JsonResponse
from .forms import LocatarioForm
import logging
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

logger = logging.getLogger(__name__)

def listar_locatarios(request):
    search_query = request.GET.get('search', '').lower()
    ordenar_por = request.GET.get('ordenar_por', 'l.Nome')  # Ordena por Nome por padrão
    with connection.cursor() as cursor:
        if search_query:
            cursor.execute(f"""
                SELECT l.ID_Locatario, l.Nome, l.Telefone, l.RG, l.CPF_CNPJ, ec.Desc_Estado_Civil
                FROM Locatario l
                LEFT JOIN Estado_Civil ec ON l.ID_Estado_Civil = ec.ID_Estado_Civil
                WHERE LOWER(l.Nome) LIKE %s
                ORDER BY {ordenar_por} ASC
            """, [f'%{search_query}%'])
        else:
            cursor.execute(f"""
                SELECT l.ID_Locatario, l.Nome, l.Telefone, l.RG, l.CPF_CNPJ, ec.Desc_Estado_Civil
                FROM Locatario l
                LEFT JOIN Estado_Civil ec ON l.ID_Estado_Civil = ec.ID_Estado_Civil
                ORDER BY {ordenar_por} ASC
            """)
        locatarios = cursor.fetchall()
    return render(request, 'locatarios/listar.html', {'locatarios': locatarios, 'search_query': search_query, 'ordenar_por': ordenar_por})

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
                    messages.success(request, 'Locatário cadastrado com sucesso!')
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
                    messages.success(request, 'Locatário editado com sucesso!')
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

@csrf_protect
def excluir_locatario(request, id_locatario):
    logger.debug(f"Tentando excluir o locatário com ID: {id_locatario}")
    
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.callproc("excluir_locatario", [id_locatario])
            
            logger.debug(f"Locatário com ID: {id_locatario} excluído com sucesso")
            return JsonResponse({"success": True})
        
        except Exception as e:
            logger.error(f"Erro ao excluir o locatário com ID: {id_locatario} - {str(e)}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    logger.error(f"Método inválido para excluir o locatário com ID: {id_locatario}")
    return JsonResponse({"success": False, "error": "Método inválido"}, status=400)


def visualizar_locatario(request, id_locatario):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT l.ID_Locatario, l.Nome, l.Telefone, l.RG, l.CPF_CNPJ, ec.Desc_Estado_Civil
                FROM Locatario l
                LEFT JOIN Estado_Civil ec ON l.ID_Estado_Civil = ec.ID_Estado_Civil
                WHERE l.ID_Locatario = %s
            """, [id_locatario])
            locatario = cursor.fetchone()
            if locatario is None:
                return HttpResponse("Locatário não encontrado", status=404)
            return render(request, 'locatarios/visualizar.html', {'locatario': locatario})
    except Exception as e:
        return HttpResponse(f"Erro ao visualizar locatário: {e}", status=500)
