from django.urls import path
from . import views

urlpatterns = [
  path('queried_articles', views.queried_articles, name='queried_articles'),
  path('accounts/logout/', views.logout_view, name='logout'),
  path('', views.home, name='home'),
  path('article/save_article', views.save_article, name="save_article")
]