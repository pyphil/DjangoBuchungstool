from django.urls import path
from . import views


urlpatterns = [
    path('<str:room>/', views.devicelist, name='devicelist'),
    path('deviceEntry/<str:room>/<str:date>/<int:std>/', views.devicelistEntryNew, name='deviceEntryNew'),
    path('deviceEntry/<str:room>/<str:date>/<int:std>/<str:dev>/', views.devicelistEntry, name='deviceEntry'),
    path('deviceUsers/<str:room>/<str:date>/<str:dev>/', views.lastDeviceUsers, name='deviceusers'),
]
