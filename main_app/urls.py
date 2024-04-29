from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('accounts/logout/', views.logout_view, name='logout'),
]