from django.contrib import admin
from django.urls import path
from monitor import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('historico/', views.historico, name='historico'),
    path('incidentes-ativos/', views.incidentes_ativos, name='incidentes_ativos'),
    path('registrar-novo/', views.registrar_incidente, name='registrar_novo'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('gerenciar/', views.gerenciar_incidentes, name='gerenciar_incidentes'),
    path('gerenciar/<int:incidente_id>/', views.editar_incidente, name='editar_incidente'),
]