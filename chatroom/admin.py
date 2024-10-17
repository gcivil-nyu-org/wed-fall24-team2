from django.contrib import admin

from .models import Explorer, Chatroom, Message

admin.site.register(Explorer)
admin.site.register(Chatroom)
admin.site.register(Message)
