import csv

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from apps.utils.excel_reader import get_contratos_data


def index(request):
    try:
        data = get_contratos_data()
        error = None
    except FileNotFoundError as e:
        data = None
        error = str(e)

    context = {
        'data': data,
        'error': error,
    }
    return render(request, 'contratos/index.html', context)


def api_data(request):
    try:
        data = get_contratos_data()
        return JsonResponse(data, safe=False)
    except FileNotFoundError as e:
        return JsonResponse({'error': str(e)}, status=404)


def export_csv(request):
    try:
        data = get_contratos_data()
    except FileNotFoundError as e:
        return HttpResponse(str(e), status=404)

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="alteracoes_orcamentarias.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Programa (Anulado)', 'Projeto (Anulado)', 'Ficha (Anulado)',
        'Programa (Suplementado)', 'Projeto (Suplementado)', 'Ficha (Suplementado)',
        'Valor', 'Justificativa',
    ])
    for r in data['records']:
        writer.writerow([
            r['programa_anulado'], r['projeto_anulado'], r['ficha_anulado'],
            r['programa_suplementado'], r['projeto_suplementado'], r['ficha_suplementado'],
            r['valor'], r['justificativa'],
        ])
    return response
