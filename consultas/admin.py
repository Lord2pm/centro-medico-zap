from django.contrib import admin

from .models import Consulta, TipoConsulta

admin.site.register(TipoConsulta)
admin.site.register(Consulta)
