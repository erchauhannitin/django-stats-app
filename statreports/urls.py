from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.stats, name='stats'),
    path('chars/', views.chars, name='chars'),
    path('file_input/', views.file_input, name='file_input'),

]
