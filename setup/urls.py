from django.contrib import admin
from django.urls import path
from monitor.views import index
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='monitor/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
