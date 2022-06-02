from django.urls import path
from . import views


urlpatterns = [
    path('<str:room>/', views.devicelist, name='devicelist'),
    path('deviceUsers/<str:room>/<str:date>/<str:dev>/', views.lastDeviceUsers, name='deviceusers'),
    path('deviceEntry/<str:room>/<str:date>/<str:dev>/', views.devicelistEntry, name='deviceEntry'),
]