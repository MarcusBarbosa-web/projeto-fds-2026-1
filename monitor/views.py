from django.shortcuts import render

def index(request):
    return render(request, 'monitor/index.html')

def historico(request):
    return render(request, 'monitor/historico.html')

def incidentes_ativos(request):
    return render(request, 'monitor/incidentes_ativos.html')