from django.urls import path
from .views.views_stats import stats
from .views.views_chars import chars
from .views.views_stats import home


urlpatterns = [
    path('stats/', stats, name='stats'),
    path('chars/', chars, name='chars'),
    path('', home, name='home'),
]
