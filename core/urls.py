from django.contrib import admin
from django.urls import path, include
from .views import home, show_start_message, show_menu, close_session

urlpatterns = [
    path("", home, name="home"),
    path("show-start-message/", show_start_message, name="start"),
    path("show-menu/", show_menu, name="menu"),
    path("close-session/", close_session, name="close-session"),
    path("admin/", admin.site.urls),
    path("consultas/", include("consultas.urls")),
]
