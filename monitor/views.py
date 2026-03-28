from django.shortcuts import render, redirect
from .models import Incidente

def index(request):
    incidentes = Incidente.objects.all().order_by('-data_criacao')
    return render(request, 'monitor/index.html', {'incidentes': incidentes})

def historico(request):
    return render(request, 'monitor/historico.html')

def registrar_incidente(request):
    return render(request, 'monitor/registrar_novo.html')

def incidentes_ativos(request): 

    if request.method == 'POST':
        
        sistema_form = request.POST.get('sistema')
        status_form = request.POST.get('status') 
        descricao_form = request.POST.get('descricao')

        novo_incidente = Incidente(
            sistema=sistema_form,
            status=status_form,
            descricao=descricao_form
        )
        novo_incidente.save()

        return redirect('index')

    return render(request, 'monitor/incidentes_ativos.html')