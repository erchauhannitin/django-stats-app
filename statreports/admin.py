from django.contrib import admin
from .models import ClientRow, ServerRow, AlarmRow, PathRow

admin.site.register(ClientRow)
admin.site.register(ServerRow)
admin.site.register(AlarmRow)
admin.site.register(PathRow)
