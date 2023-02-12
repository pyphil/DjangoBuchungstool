from django.urls import path
from . import views


urlpatterns = [
    path('', views.settings, name='settings'),
    path('frontpage_alert/', views.settings_frontpage_alert, name='settings_frontpage_alert'),
]
