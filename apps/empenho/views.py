import csv

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from apps.utils.excel_reader import get_empenho_data


def index(request):
    empresa_filter = request.GET.get('empresa', '').strip().upper()

    try:
        data = get_empenho_data()
        error = None
    except FileNotFoundError as e:
        data = None
        error = str(e)

    records = []
    if data:
        records = data['records']
        if empresa_filter:
            records = [r for r in records if empresa_filter in (r['empresa'] or '').upper()]

    context = {
        'data': data,
        'records': records,
        'error': error,
        'empresa_filter': empresa_filter,
    }
    return render(request, 'empenho/index.html', context)


def api_data(request):
    try:
        data = get_empenho_data()
        return JsonResponse(data, safe=False)
    except FileNotFoundError as e:
        return JsonResponse({'error': str(e)}, status=404)


def export_csv(request):
    try:
        data = get_empenho_data()
    except FileNotFoundError as e:
        return HttpResponse(str(e), status=404)

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="empenho_2025.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Data', 'Programa', 'Ficha', 'Ação', 'Projeto', 'Reserva',
        'Cód. Empresa', 'Empresa', 'Empenho', 'Valor Empenho',
        'Estorno', 'Saldo Empenho', 'Liquidado', 'Saldo',
    ])
    for r in data['records']:
        writer.writerow([
            r['data'], r['programa'], r['ficha'], r['acao'], r['projeto'], r['reserva'],
            r['cod_empresa'], r['empresa'], r['empenho'], r['valor_empenho'],
            r['estorno'], r['saldo_empenho'], r['liquidado'], r['saldo'],
        ])
    return response
