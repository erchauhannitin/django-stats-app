from django.urls import path
from .views.views_stats import stats
from .views.views_chars import chars
from .views.views_stats import home
from .views.views_chars import home_char

urlpatterns = [
    path('stats/', stats, name='stats'),
    path('chars/', chars, name='chars'),
    path('home_char', home_char, name='home_char'),
    path('', home, name='home'),
]
