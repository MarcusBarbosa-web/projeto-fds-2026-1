from django.shortcuts import render, redirect
from .models import Incidente
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

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

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('Email')
        password = request.POST.get('password')
        user = authenticate(request, Email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'monitor/login.html', {'form': {'errors': True}})
        
    return render(request, 'monitor/login.html')