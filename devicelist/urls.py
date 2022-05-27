from django.urls import path
from . import views


urlpatterns = [
    path('<str:room>/<str:date>/<str:dev>/', views.devicelist, name='devicelist')
]