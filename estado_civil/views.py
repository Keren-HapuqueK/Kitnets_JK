from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from .forms import EstadoCivilForm
import logging

logger = logging.getLogger(__name__)

# Função genérica para executar SQL
def executar_sql(query, params=None, fetch_one=False):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                return cursor.fetchone() if fetch_one else cursor.fetchall()
    except Exception as e:
        logger.error(f"Erro ao executar SQL: {e}")
        raise

# Listar estados civis
def listar_estados_civis(request):
    search_query = request.GET.get('search', '').lower()
    try:
        if search_query:
            estados_civis = executar_sql(
                'SELECT * FROM estado_civil WHERE LOWER(desc_estado_civil) LIKE %s ORDER BY desc_estado_civil ASC',
                [f'%{search_query}%']
            )
        else:
            estados_civis = executar_sql('SELECT * FROM estado_civil ORDER BY desc_estado_civil ASC')
        return render(request, 'estado_civil/listar.html', {'estados_civis': estados_civis, 'search_query': search_query})
    except Exception as e:
        return HttpResponse(f"Erro ao listar estados civis: {e}", status=500)

# Criar estado civil
def criar_estado_civil(request):
    if request.method == 'POST':
        form = EstadoCivilForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                executar_sql("SELECT criar_estado_civil(%s)", [data['desc_estado_civil']])
                return redirect('listar_estados_civis')
            except Exception as e:
                return HttpResponse(f"Erro ao criar estado civil: {e}", status=500)
        else:
            return render(request, 'estado_civil/criar.html', {'form': form})
    else:
        form = EstadoCivilForm()
    return render(request, 'estado_civil/criar.html', {'form': form})

# Editar estado civil
def editar_estado_civil(request, id_estado_civil):
    if request.method == 'POST':
        form = EstadoCivilForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                executar_sql("SELECT editar_estado_civil(%s, %s)", [id_estado_civil, data['desc_estado_civil']])
                return redirect('listar_estados_civis')
            except Exception as e:
                return HttpResponse(f"Erro ao editar estado civil: {e}", status=500)
        else:
            return render(request, 'estado_civil/editar.html', {'form': form})
    else:
        estado_civil = executar_sql("SELECT * FROM estado_civil WHERE id_estado_civil = %s", [id_estado_civil], fetch_one=True)
        if not estado_civil:
            return HttpResponse("Estado civil não encontrado.", status=404)

        form = EstadoCivilForm(initial={'desc_estado_civil': estado_civil[1]})
    return render(request, 'estado_civil/editar.html', {'form': form})

# Excluir estado civil
def excluir_estado_civil(request, id_estado_civil):
    if request.method == 'POST':
        try:
            executar_sql("SELECT excluir_estado_civil(%s)", [id_estado_civil])
            return redirect('listar_estados_civis')
        except Exception as e:
            return HttpResponse(f"Erro ao excluir estado civil: {e}", status=500)
    return render(request, 'estado_civil/excluir.html', {'id_estado_civil': id_estado_civil})
