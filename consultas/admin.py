from django.contrib import admin

from .models import Consulta, TipoConsulta

admin.site.site_header = "Painel Administrativo - Clínica Visão Futurista"
admin.site.site_title = "Painel Administrativo - Clínica Visão Futurista"
admin.site.index_title = "Bem-vindo ao Painel de Administração"

admin.site.register(TipoConsulta)
admin.site.register(Consulta)
