import csv
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from apps.utils.excel_reader import get_liquidacao_data


def index(request):
    status_filter = request.GET.get('status', '')
    empresa_filter = request.GET.get('empresa', '').strip().upper()

    try:
        data = get_liquidacao_data()
        error = None
    except FileNotFoundError as e:
        data = None
        error = str(e)

    records = []
    if data:
        records = data['records']
        if status_filter:
            records = [r for r in records if r['status'] == status_filter]
        if empresa_filter:
            records = [r for r in records if empresa_filter in (r['empresa'] or '').upper()]

    context = {
        'data': data,
        'records': records,
        'error': error,
        'status_filter': status_filter,
        'empresa_filter': empresa_filter,
        'status_opcoes': ['PAGO', 'ATRASADO', 'NO PRAZO'],
    }
    return render(request, 'liquidacao/index.html', context)


API_RECORDS_LIMIT = 200


def api_data(request):
    try:
        data = get_liquidacao_data()
        data['records'] = data['records'][:API_RECORDS_LIMIT]
        return JsonResponse(data, safe=False)
    except FileNotFoundError as e:
        return JsonResponse({'error': str(e)}, status=404)


def export_csv(request):
    try:
        data = get_liquidacao_data()
    except FileNotFoundError as e:
        return HttpResponse(str(e), status=404)

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="liquidacao_2025.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Data Liquidação', 'Cód. Empresa', 'Empresa', 'Processo', 'Contrato',
        'Empenho', 'NF', 'Mês Desembolso', 'Período Inicial', 'Período Final',
        'Valor Bruto', 'Valor Retenção', 'Valor Líquido', 'Vencimento',
        'Valores Pagos', 'Pagto', 'Status', 'Dias Atraso', 'Previsão Pagto',
    ])
    for r in data['records']:
        writer.writerow([
            r['data_liquid'], r['cod_empresa'], r['empresa'], r['processo'], r['contrato'],
            r['empenho'], r['nf'], r['mes_desembolso'], r['periodo_inicial'], r['periodo_final'],
            r['valor_bruto'], r['valor_retencao'], r['valor_liquido'], r['vencimento'],
            r['valores_pagos'], r['pagto'], r['status'], r['dias_atraso'], r['previsao_pagto'],
        ])
    return response
