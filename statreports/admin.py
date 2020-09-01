from django.contrib import admin
from .models import ClientRow, ServerRow, AlarmRow, CharsRow, ClientParentRow, ClientParentHistoryRow

admin.site.register(ClientRow)
admin.site.register(ServerRow)
admin.site.register(AlarmRow)
admin.site.register(CharsRow)
admin.site.register(ClientParentRow)
admin.site.register(ClientParentHistoryRow)
