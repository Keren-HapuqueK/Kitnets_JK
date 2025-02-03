from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse

from .forms import ContratoForm


# Função para executar uma query no banco de dados
def executar_query(query, parametros=None, fetchone=False, fetchall=False):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, parametros or [])
            if fetchone:
                return cursor.fetchone()
            elif fetchall:
                return cursor.fetchall()
    except Exception as e:
        raise RuntimeError(f"Erro na execução da query: {e}")

def listar_contratos(request):
    search_query = request.GET.get('search', '').lower()
    ordenar_por = request.GET.get('ordenar_por', 'NU_Contrato')  # Ordena por NU_Contrato por padrão
    try:
        with connection.cursor() as cursor:
            if search_query:
                query = f"""
                    SELECT c.ID_Contrato, c.NU_Contrato, c.VLR_Aluguel, c.DT_Inicio, c.Dia_Base, c.DT_Fim, c.Cidade, c.UF,
                           i.Endereco, l.Nome, loc.Nome
                    FROM Contrato c
                    JOIN Imovel i ON c.ID_Imovel = i.ID_Imovel
                    JOIN Locatario l ON c.ID_Locatario = l.ID_Locatario
                    JOIN Locador loc ON c.ID_Locador = loc.ID_Locador
                    WHERE LOWER(c.NU_Contrato) LIKE %s
                    ORDER BY {ordenar_por} ASC
                """
                cursor.execute(query, [f'%{search_query}%'])
            else:
                query = f"""
                    SELECT c.ID_Contrato, c.NU_Contrato, c.VLR_Aluguel, c.DT_Inicio, c.Dia_Base, c.DT_Fim, c.Cidade, c.UF,
                           i.Endereco, l.Nome, loc.Nome
                    FROM Contrato c
                    JOIN Imovel i ON c.ID_Imovel = i.ID_Imovel
                    JOIN Locatario l ON c.ID_Locatario = l.ID_Locatario
                    JOIN Locador loc ON c.ID_Locador = loc.ID_Locador
                    ORDER BY {ordenar_por} ASC
                """
                cursor.execute(query)
            contratos = cursor.fetchall()
            return render(request, 'contratos/listar.html', {'contratos': contratos, 'search_query': search_query})
    except Exception as e:
        return HttpResponse(f"Erro ao listar contratos: {e}", status=500)

def criar_contrato(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('criar_contrato', [
                        data['nu_contrato'],
                        data['vlr_aluguel'],
                        data['dt_inicio'],
                        data['dia_base'],
                        data['dt_fim'],
                        data['cidade'],
                        data['uf'],
                        data['id_imovel'],
                        data['id_locatario'],
                        data['id_locador']
                    ])
                    return redirect('listar_contratos')  # Redireciona para a listagem
            except Exception as e:
                return HttpResponse(f"Erro ao criar contrato: {e}", status=500)
    else:
        form = ContratoForm()
    return render(request, 'contratos/criar.html', {'form': form})


def editar_contrato(request, id_contrato):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('editar_contrato', [
                        id_contrato,
                        data['nu_contrato'],
                        data['vlr_aluguel'],
                        data['dt_inicio'],
                        data['dia_base'],
                        data['dt_fim'],
                        data['cidade'],
                        data['uf'],
                        data['id_imovel'],
                        data['id_locatario'],
                        data['id_locador']
                    ])
                    return redirect('listar_contratos')
            except Exception as e:
                return HttpResponse(f"Erro ao editar contrato: {e}", status=500)
    else:
        contrato = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.ID_Contrato, c.NU_Contrato, c.VLR_Aluguel, c.DT_Inicio, c.Dia_Base, c.DT_Fim, c.Cidade, c.UF,
                           i.ID_Imovel, l.ID_Locatario, loc.ID_Locador
                    FROM Contrato c
                    JOIN Imovel i ON c.ID_Imovel = i.ID_Imovel
                    JOIN Locatario l ON c.ID_Locatario = l.ID_Locatario
                    JOIN Locador loc ON c.ID_Locador = loc.ID_Locador
                    WHERE c.ID_Contrato = %s
                """, [id_contrato])
                contrato = cursor.fetchone()
        except Exception as e:
            return HttpResponse(f"Erro ao carregar contrato: {e}", status=500)

        if contrato is None:
            return HttpResponse("Contrato não encontrado", status=404)

        form = ContratoForm(initial={
            'nu_contrato': contrato[1],
            'vlr_aluguel': contrato[2],
            'dt_inicio': contrato[3],
            'dia_base': contrato[4],
            'dt_fim': contrato[5],
            'cidade': contrato[6],
            'uf': contrato[7],
            'id_imovel': contrato[8],
            'id_locatario': contrato[9],
            'id_locador': contrato[10]
        })
    return render(request, 'contratos/editar.html', {'form': form})

def excluir_contrato(request, id_contrato):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('excluir_contrato', [id_contrato])
                return redirect('listar_contratos')
        except Exception as e:
            return HttpResponse(f"Erro ao excluir contrato: {e}", status=500)
    return render(request, 'contratos/excluir.html', {'id_contrato': id_contrato})

def visualizar_contrato(request, id_contrato):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.ID_Contrato, c.NU_Contrato, c.VLR_Aluguel, c.DT_Inicio, c.Dia_Base, c.DT_Fim, c.Cidade, c.UF,
                       i.Endereco, l.Nome, loc.Nome
                FROM Contrato c
                JOIN Imovel i ON c.ID_Imovel = i.ID_Imovel
                JOIN Locatario l ON c.ID_Locatario = l.ID_Locatario
                JOIN Locador loc ON c.ID_Locador = loc.ID_Locador
                WHERE c.ID_Contrato = %s
            """, [id_contrato])
            contrato = cursor.fetchone()
            return render(request, 'contratos/visualizar.html', {'contrato': contrato})
    except Exception as e:
        return HttpResponse(f"Erro ao visualizar contrato: {e}", status=500)
