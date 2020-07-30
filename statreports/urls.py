from django.urls import path
from . import views

urlpatterns = [
    path('', views.stats, name='index'),
    path('all/', views.all, name='all'),

]
