from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('password-change/', views.change_password, name='change_password'),
    path('creater_details/<str:username>/', views.creater_details, name='creater_details'),
    path('about/',views.aboutme, name='aboutme')
]
