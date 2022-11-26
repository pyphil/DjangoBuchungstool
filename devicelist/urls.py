from django.urls import path
from . import views


urlpatterns = [
    path('<str:room>/<str:date>/<int:std>/<int:entry_id>/', views.devicelist, name='devicelist'),
    path('admin/', views.devicelist_admin, name='devicelist_admin'),
    path('deviceEntry/<str:room>/<str:date>/<int:std>/<int:entry_id>/', views.devicelistEntryNew, name='deviceEntryNew'),
    path('deviceEntry/<int:id>/<str:room>/<str:date>/<int:std>/<int:entry_id>/', views.devicelistEntry, name='deviceEntry'),
    path('deviceUsers/<str:room>/<str:date>/<str:dev>/', views.lastDeviceUsers, name='deviceusers'),
]
