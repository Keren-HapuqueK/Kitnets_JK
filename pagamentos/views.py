from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from .forms import RegistroPagamentoForm


def listar_pagamentos(request):
    search_query = request.GET.get('search', '').lower()
    ordenar_por = request.GET.get('ordenar_por', 'rp.DT_Paga')  # Ordena por DT_Paga por padrão
    with connection.cursor() as cursor:
        if search_query:
            cursor.execute(f"""
                SELECT rp.ID_Pagamento, rp.DT_Paga, rp.Ref_Mes_Ano, rp.Observacao, c.NU_Contrato, l.Nome, fp.Desc_Forma_Pgto
                FROM Registro_Pagamento rp
                LEFT JOIN Contrato c ON rp.ID_Contrato = c.ID_Contrato
                LEFT JOIN Locatario l ON rp.ID_Locatario = l.ID_Locatario
                LEFT JOIN Forma_Pagamento fp ON rp.ID_Forma_Pagamento = fp.ID_Forma_Pagamento
                WHERE LOWER(rp.Ref_Mes_Ano) LIKE %s
                ORDER BY {ordenar_por} ASC
            """, [f'%{search_query}%'])
        else:
            cursor.execute(f"""
                SELECT rp.ID_Pagamento, rp.DT_Paga, rp.Ref_Mes_Ano, rp.Observacao, c.NU_Contrato, l.Nome, fp.Desc_Forma_Pgto
                FROM Registro_Pagamento rp
                LEFT JOIN Contrato c ON rp.ID_Contrato = c.ID_Contrato
                LEFT JOIN Locatario l ON rp.ID_Locatario = l.ID_Locatario
                LEFT JOIN Forma_Pagamento fp ON rp.ID_Forma_Pagamento = fp.ID_Forma_Pagamento
                ORDER BY {ordenar_por} ASC
            """)
        pagamentos = cursor.fetchall()
    pagamentos = [
        {
            'id': p[0],
            'data_pagamento': p[1],
            'referencia': p[2],
            'contrato': {'nome': p[4]},
            'locatario': {'nome': p[5]},
            'forma_pagamento': {'nome': p[6]},
            'observacao': p[3]
        }
        for p in pagamentos
    ]
    return render(request, 'pagamentos/listar.html', {'pagamentos': pagamentos, 'search_query': search_query, 'ordenar_por': ordenar_por})

def criar_pagamento(request):
    if request.method == 'POST':
        form = RegistroPagamentoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('criar_pagamento', [
                        data['dt_paga'],
                        data['ref_mes_ano'],
                        data['observacao'],
                        data['id_contrato'],
                        data['id_locatario'],
                        data['id_forma_pagamento']
                    ])
                    return redirect('listar_pagamentos')  # Redireciona para a listagem
            except Exception as e:
                return HttpResponse(f"Erro ao criar pagamento: {e}", status=500)
    else:
        form = RegistroPagamentoForm()
    return render(request, 'pagamentos/criar.html', {'form': form})

def editar_pagamento(request, id_pagamento):
    if request.method == 'POST':
        form = RegistroPagamentoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('editar_pagamento', [
                        id_pagamento,
                        data['dt_paga'],
                        data['ref_mes_ano'],
                        data['observacao'],
                        data['id_contrato'],
                        data['id_locatario'],
                        data['id_forma_pagamento']
                    ])
                    return redirect('listar_pagamentos')  # Redireciona para a listagem
            except Exception as e:
                return HttpResponse(f"Erro ao editar pagamento: {e}", status=500)
    else:
        pagamento = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT rp.ID_Pagamento, rp.DT_Paga, rp.Ref_Mes_Ano, rp.Observacao, rp.ID_Contrato, rp.ID_Locatario, rp.ID_Forma_Pagamento
                    FROM Registro_Pagamento rp
                    WHERE rp.ID_Pagamento = %s
                """, [id_pagamento])
                pagamento = cursor.fetchone()
        except Exception as e:
            return HttpResponse(f"Erro ao carregar pagamento: {e}", status=500)

        if pagamento is None:
            return HttpResponse("Pagamento não encontrado", status=404)

        form = RegistroPagamentoForm(initial={
            'dt_paga': pagamento[1].strftime('%Y-%m-%d') if pagamento[1] else '',
            'ref_mes_ano': pagamento[2],
            'observacao': pagamento[3],
            'id_contrato': pagamento[4],
            'id_locatario': pagamento[5],
            'id_forma_pagamento': pagamento[6]
        })
    return render(request, 'pagamentos/editar.html', {'form': form})

def excluir_pagamento(request, id_pagamento):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('excluir_pagamento', [id_pagamento])
                return redirect('listar_pagamentos')  # Redireciona para a listagem
        except Exception as e:
            return HttpResponse(f"Erro ao excluir pagamento: {e}", status=500)
    else:
        pagamento = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Registro_Pagamento WHERE ID_Pagamento = %s", [id_pagamento])
                pagamento = cursor.fetchone()
        except Exception as e:
            return HttpResponse(f"Erro ao carregar pagamento: {e}", status=500)

        if pagamento is None:
            return HttpResponse("Pagamento não encontrado", status=404)

        return render(request, 'pagamentos/excluir.html', {'pagamento': pagamento})

def visualizar_pagamento(request, id_pagamento):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT rp.ID_Pagamento, rp.DT_Paga, rp.Ref_Mes_Ano, rp.Observacao, 
                       c.NU_Contrato, l.Nome, fp.Desc_Forma_Pgto
                FROM Registro_Pagamento rp
                LEFT JOIN Contrato c ON rp.ID_Contrato = c.ID_Contrato
                LEFT JOIN Locatario l ON rp.ID_Locatario = l.ID_Locatario
                LEFT JOIN Forma_Pagamento fp ON rp.ID_Forma_Pagamento = fp.ID_Forma_Pagamento
                WHERE rp.ID_Pagamento = %s
            """, [id_pagamento])
            pagamento = cursor.fetchone()
        
        if pagamento is None:
            return HttpResponse("Pagamento não encontrado", status=404)

        return render(request, 'pagamentos/visualizar.html', {'pagamento': pagamento})
    
    except Exception as e:
        return HttpResponse(f"Erro ao visualizar pagamento: {e}", status=500)