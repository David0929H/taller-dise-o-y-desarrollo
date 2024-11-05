"""
URL configuration for rutaculinaria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ayua import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mostrar_inicio, name='pagina_principal'),
    path('login_cliente/', views.login_cliente, name='login_cliente'),
    path('login_admin/', views.login_admin, name='login_admin'),
    path('registro_cliente/', views.registro_cliente, name='registro_cliente'),
    path('perfil_cliente/', views.perfil_cliente, name='perfil_cliente'),
    path('administrador/', views.pantalla_admin, name='ordenes'),
    path('orden_actual/', views.orden_actual, name='orden_actual'),
    path('ordenes/', views.todas_ordenes, name='ordenes'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('finalizar/', views.finalizar_pedido, name='finalizar_pedido'),
    path('menu_admin/', views.pantalla_admin, name='menu_admin'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
