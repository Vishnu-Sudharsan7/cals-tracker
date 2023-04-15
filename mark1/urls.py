"""mark1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include

urlpatterns = [
    path('', include('test1.urls')),
    path('signup', include('test1.urls')),
    path('create', include('test1.urls')),
    path('home1', include('test1.urls')),
    path('track', include('test1.urls')),
    path('log',include('test1.urls')),
    path('cals_track', include('test1.urls')),
    path('logincheck', include('test1.urls')),
    path('add_details', include('test1.urls')),
    path('admin/', admin.site.urls),
]
