"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('crear', views.home, name="crear"),
    path('read', views.read, name="read"),
    path('vista_previa_solicitud/<int:id>', views.vista_previa_solicitud, name="vista_previa_solicitud"),
    path('vista_previa_respuesta/<int:id>/', views.vista_previa_respuesta, name='vista_previa_respuesta'),
    path('respuesta/<int:id>', views.respuesta, name="respuesta"),    
    path('respuesta_edit/<int:id>', views.respuesta_edit, name="respuesta_edit"),
    path('amparo/<int:id>', views.respuesta, name="amparo"),
    path('prorroga/<int:id>/', views.prorroga, name='prorroga'),
    path('accion/editar_solicitud/<int:id>/', views.editar_solicitud, name='editar_solicitud'),
    path('editar_solicitud/<int:solicitud_id>/', views.editar_solicitud, name='editar_solicitud'),
    path('autocomplete_persona/', views.autocomplete_persona, name='autocomplete_persona'),
    # Otras rutas...
]
