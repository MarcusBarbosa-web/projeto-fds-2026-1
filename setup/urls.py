from django.contrib import admin
from django.urls import path, include
from monitor import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='monitor/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('historico/', views.historico, name='historico'),
    path('incidentes-ativos/', views.incidentes_ativos, name='incidentes_ativos'),
]
