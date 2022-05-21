"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from buchungstool import views as buchungstoolViews
from userlist import views as userlistViews
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', buchungstoolViews.rooms, name='buchungstoolRooms'),
    path('buchungstool/', buchungstoolViews.home, name='buchungstoolHome'),
    path('buchungstool/<str:room>', buchungstoolViews.home, name='buchungstoolHome'),
    path('buchungstool/entry/', buchungstoolViews.eintrag, name='buchungstoolEntry'),
    path('buchungstool/entry/<int:id>', buchungstoolViews.eintrag, name='buchungstoolEntry'),
    path('userlist/select/', userlistViews.select, name='userlistSelect'),
    path('userlist/entry/', userlistViews.entry, name='userlistEntry'),
    path('userlist/success/', userlistViews.success, name='userlistSuccess'),
    path('tinymce/', include('tinymce.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
