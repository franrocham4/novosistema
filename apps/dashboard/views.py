from django.shortcuts import render
from apps.utils.excel_reader import get_dashboard_data


def index(request):
    try:
        data = get_dashboard_data()
        error = None
    except FileNotFoundError as e:
        data = None
        error = str(e)

    context = {
        'data': data,
        'error': error,
    }
    return render(request, 'dashboard/index.html', context)
