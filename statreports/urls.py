from django.urls import include, path
from .views.views_stats import stats
from .views.views_chars import chars
from .views.views_chars import home_char
from .views.views_stats import home_stat
from .views.views_char_summary import char_json
from .views.views_char_summary import char_chart
from .views.views_clientparent_summary import clientparent_json
from .views.views_clientparent_summary import clientparent_chart
from .views.views_history import history
from .views.views_summary import summary
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
    path('stats/', stats, name='stats'),
    path('chars/', chars, name='chars'),
    path('home_char', home_char, name='home_char'),
    path('home_stat', home_stat, name='home_stat'),

    path('char_json/', char_json, name='char_json'),
    path('char_chart/', char_chart, name='char_chart'),

    path('clientparent_json/', clientparent_json, name='clientparent_json'),
    path('clientparent_chart/', clientparent_chart, name='clientparent_chart'),

    path('summary/', summary, name='summary'),
    path('history/', history, name='history'),

    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('images/favicon.ico')))

]
