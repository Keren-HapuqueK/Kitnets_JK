from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from .forms import RegistroPagamentoForm, FormaPagamentoForm

def listar_pagamentos(request):
    search_query = request.GET.get('search', '').lower()
    with connection.cursor() as cursor:
        if search_query:
            cursor.execute("""
                SELECT rp.ID_Pagamento, rp.DT_Paga, rp.Ref_Mes_Ano, rp.Observacao, c.NU_Contrato, l.Nome, fp.Desc_Forma_Pgto
                FROM Registro_Pagamento rp
                LEFT JOIN Contrato c ON rp.ID_Contrato = c.ID_Contrato
                LEFT JOIN Locatario l ON rp.ID_Locatario = l.ID_Locatario
                LEFT JOIN Forma_Pagamento fp ON rp.ID_Forma_Pagamento = fp.ID_Forma_Pagamento
                WHERE LOWER(rp.Ref_Mes_Ano) LIKE %s
                ORDER BY rp.DT_Paga ASC
            """, [f'%{search_query}%'])
        else:
            cursor.execute("""
                SELECT rp.ID_Pagamento, rp.DT_Paga, rp.Ref_Mes_Ano, rp.Observacao, c.NU_Contrato, l.Nome, fp.Desc_Forma_Pgto
                FROM Registro_Pagamento rp
                LEFT JOIN Contrato c ON rp.ID_Contrato = c.ID_Contrato
                LEFT JOIN Locatario l ON rp.ID_Locatario = l.ID_Locatario
                LEFT JOIN Forma_Pagamento fp ON rp.ID_Forma_Pagamento = fp.ID_Forma_Pagamento
                ORDER BY rp.DT_Paga ASC
            """)
        pagamentos = cursor.fetchall()
    pagamentos = [
        {
            'id': p[0],
            'data_pagamento': p[1],
            'referencia': p[2],
            'observacao': p[3],
            'contrato': {'nome': p[4]},
            'locatario': {'nome': p[5]},
            'forma_pagamento': {'nome': p[6]}
        }
        for p in pagamentos
    ]
    return render(request, 'pagamentos/listar.html', {'pagamentos': pagamentos, 'search_query': search_query})

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
            'dt_paga': pagamento[1],
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

def listar_formas_pagamento(request):
    search_query = request.GET.get('search', '').lower()
    with connection.cursor() as cursor:
        if search_query:
            cursor.execute("""
                SELECT * FROM Forma_Pagamento
                WHERE LOWER(desc_forma_pgto) LIKE %s
                ORDER BY desc_forma_pgto ASC
            """, [f'%{search_query}%'])
        else:
            cursor.execute("SELECT * FROM Forma_Pagamento ORDER BY desc_forma_pgto ASC")
        formas_pagamento = cursor.fetchall()
    return render(request, 'forma_pagamento/listar.html', {'formas_pagamento': formas_pagamento, 'search_query': search_query})

def criar_forma_pagamento(request):
    if request.method == 'POST':
        form = FormaPagamentoForm(request.POST)
        if form.is_valid():
            desc_forma_pgto = form.cleaned_data['desc_forma_pgto']
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('criar_forma_pagamento', [desc_forma_pgto])
                    return redirect('listar_formas_pagamento')
            except Exception as e:
                return HttpResponse(f"Erro ao adicionar forma de pagamento: {e}", status=500)
    else:
        form = FormaPagamentoForm()
    return render(request, 'forma_pagamento/criar.html', {'form': form})

def editar_forma_pagamento(request, id_forma_pagamento):
    if request.method == 'POST':
        form = FormaPagamentoForm(request.POST)
        if form.is_valid():
            desc_forma_pgto = form.cleaned_data['desc_forma_pgto']
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('editar_forma_pagamento', [id_forma_pagamento, desc_forma_pgto])
                    return redirect('listar_formas_pagamento')
            except Exception as e:
                return HttpResponse(f"Erro ao editar forma de pagamento: {e}", status=500)
    else:
        forma_pagamento = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Forma_Pagamento WHERE ID_Forma_Pagamento = %s", [id_forma_pagamento])
                forma_pagamento = cursor.fetchone()
        except Exception as e:
            return HttpResponse(f"Erro ao carregar forma de pagamento: {e}", status=500)

        if forma_pagamento is None:
            return HttpResponse("Forma de pagamento não encontrada", status=404)

        form = FormaPagamentoForm(initial={'desc_forma_pgto': forma_pagamento[1]})
    return render(request, 'forma_pagamento/editar.html', {'form': form})

def excluir_forma_pagamento(request, id_forma_pagamento):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('excluir_forma_pagamento', [id_forma_pagamento])
                return redirect('listar_formas_pagamento')
        except Exception as e:
            return HttpResponse(f"Erro ao excluir forma de pagamento: {e}", status=500)
    else:
        forma_pagamento = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Forma_Pagamento WHERE ID_Forma_Pagamento = %s", [id_forma_pagamento])
                forma_pagamento = cursor.fetchone()
        except Exception as e:
            return HttpResponse(f"Erro ao carregar forma de pagamento: {e}", status=500)

        if forma_pagamento is None:
            return HttpResponse("Forma de pagamento não encontrada", status=404)

        return render(request, 'forma_pagamento/excluir.html', {'forma_pagamento': forma_pagamento})
