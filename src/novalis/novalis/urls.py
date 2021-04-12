"""novalis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from filebrowser.sites import site
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from pages.views import home_view
from users.views import login_view, logout_view, gatekeeper_view



urlpatterns = [
    path('', include('posts.urls')),
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('', include('users.urls')),
    path('gatekeeper/', gatekeeper_view, name='gatekeeper'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
