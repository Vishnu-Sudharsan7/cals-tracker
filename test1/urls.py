from django.urls import path
from .import views
urlpatterns=[
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('create', views.create, name='create'),
    path('home1', views.home1, name='home1'),
    path('cals_track', views.cals_track, name='cals_track'),
    path('logincheck', views.logincheck, name='logincheck'),
    path('add_details', views.add_details, name='add_details')
]
