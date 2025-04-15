from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect
from .forms import ImovelForm
import logging

logger = logging.getLogger(__name__)

def listar_imoveis(request):
    search_query = request.GET.get('search', '').lower()
    ordenar_por = request.GET.get('ordenar_por', 'Endereco')

    with connection.cursor() as cursor:
        if search_query:
            cursor.execute(f"""
                SELECT ID_Imovel, ID_Locador, Endereco, Descricao, Disponivel, Vlr_Aluguel, UC
                FROM Imovel
                WHERE LOWER(Endereco) LIKE %s
                ORDER BY {ordenar_por} ASC
            """, [f'%{search_query}%'])
        else:
            cursor.execute(f"""
                SELECT ID_Imovel, ID_Locador, Endereco, Descricao, Disponivel, Vlr_Aluguel, UC
                FROM Imovel
                ORDER BY {ordenar_por} ASC
            """)
        imoveis = cursor.fetchall()
    
    return render(request, 'kitnets/listar.html', {
        'imoveis': imoveis,
        'search_query': search_query,
        'ordenar_por': ordenar_por
    })

def criar_imovel(request):
    if request.method == 'POST':
        form = ImovelForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('criar_imovel', [
                        data['id_locador'],
                        data['endereco'],
                        data['descricao'],
                        data['disponivel'],
                        data['vlr_aluguel'],
                        data['uc']
                    ])
                    return redirect('listar_imoveis')  # Redireciona para a listagem
            except Exception as e:
                return HttpResponse(f"Erro ao criar imovel: {e}", status=500)
    else:
        form = ImovelForm()
    return render(request, 'kitnets/criar.html', {'form': form})

def editar_imovel(request, id_imovel):
    if request.method == 'POST':
        form = ImovelForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('editar_imovel', [
                        id_imovel,
                        data['id_locador'],
                        data['endereco'],
                        data['descricao'],
                        data['disponivel'],
                        data['vlr_aluguel'],
                        data['uc']
                    ])
                    return redirect('listar_imoveis')  # Redireciona para a listagem
            except Exception as e:
                return HttpResponse(f"Erro ao editar imovel: {e}", status=500)
    else:
        imovel = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT ID_Imovel, ID_Locador, Endereco, Descricao, Disponivel, Vlr_Aluguel, UC FROM Imovel WHERE ID_Imovel = %s", [id_imovel])
                imovel = cursor.fetchone()
        except Exception as e:
            return HttpResponse(f"Erro ao carregar imovel: {e}", status=500)

        if imovel is None:
            return HttpResponse("Imóvel não encontrado", status=404)

        form = ImovelForm(initial={
            'id_locador': imovel[1],
            'endereco': imovel[2],
            'descricao': imovel[3],
            'disponivel': imovel[4],
            'vlr_aluguel': imovel[5],
            'uc': imovel[6]
        })
    return render(request, 'kitnets/editar.html', {'form': form})

@csrf_protect
def excluir_imovel(request, id_imovel):
    logger.debug(f"Tentando excluir o imóvel com ID: {id_imovel}")
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.callproc("excluir_imovel", [id_imovel])
            logger.debug(f"Imóvel com ID: {id_imovel} excluído com sucesso")
            return JsonResponse({"success": True})
        except Exception as e:
            logger.error(f"Erro ao excluir o imóvel com ID: {id_imovel} - {str(e)}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    logger.error(f"Método inválido para excluir o imóvel com ID: {id_imovel}")
    return JsonResponse({"success": False, "error": "Método inválido"}, status=400)


def visualizar_imovel(request, id_imovel):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT i.ID_Imovel, l.Nome, i.Endereco, i.Descricao, i.Disponivel, i.Vlr_Aluguel, i.UC
                FROM Imovel i
                JOIN Locador l ON i.ID_Locador = l.ID_Locador
                WHERE i.ID_Imovel = %s
            """, [id_imovel])
            imovel = cursor.fetchone()
            if imovel is None:
                return HttpResponse("Imóvel não encontrado", status=404)
            return render(request, 'kitnets/visualizar.html', {'imovel': imovel})
    except Exception as e:
        return HttpResponse(f"Erro ao visualizar imovel: {e}", status=500)
