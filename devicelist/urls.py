from django.urls import path
from . import views


urlpatterns = [
    path('<str:room>/', views.devicelist, name='devicelist'),
    path('<str:room>/<str:date>/<str:dev>/', views.lastDeviceUsers, name='deviceusers'),
    path('<str:room>/<str:date>/<str:dev>/', views.devicelistEntry, name='deviceEntry'),
]