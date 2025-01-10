from django.contrib import admin
from django.urls import path, include
from .views import (
    home,
    show_start_message,
    show_menu,
    close_session,
    show_about_we,
    custom_recommendations,
    schedule_appointment,
)

urlpatterns = [
    path("", home, name="home"),
    path("show-start-message/", show_start_message, name="start"),
    path("show-menu/", show_menu, name="menu"),
    path("close-session/", close_session, name="close-session"),
    path(
        "custom-recommendations/", custom_recommendations, name="custom-recommendations"
    ),
    path("show-about-we/", show_about_we, name="show-about-we"),
    path("schedule-appointment/", schedule_appointment, name="schedule-appointment"),
    path("admin/", admin.site.urls),
    path("consultas/", include("consultas.urls")),
]
