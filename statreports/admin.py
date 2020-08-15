from django.contrib import admin
from .models import ClientRow, ServerRow, AlarmRow, CharsRow, ClientParentRow

admin.site.register(ClientRow)
admin.site.register(ServerRow)
admin.site.register(AlarmRow)
admin.site.register(CharsRow)
admin.site.register(ClientParentRow)
