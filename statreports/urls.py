from django.urls import path
from .views.views_stats import stats
from .views.views_chars import chars
from .views.views_chars import home_char
from .views.views_stats import home_stat
from .views.views_charts_data import json_char_data
from .views.views_charts_data import chart_data

urlpatterns = [
    path('stats/', stats, name='stats'),
    path('chars/', chars, name='chars'),
    path('home_char', home_char, name='home_char'),
    path('home_stat', home_stat, name='home_stat'),
    path('json_char_data/', json_char_data, name='json_char_data'),
    path('json_char_data/data/', chart_data, name='chart_data'),

]
