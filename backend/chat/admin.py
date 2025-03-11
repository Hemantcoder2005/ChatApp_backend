from django.contrib import admin
from .models import *

# Register all models
admin.site.register(ChatRoom)
admin.site.register(GroupSubscription)
admin.site.register(GroupPrivileges)
admin.site.register(PersonalChatroom)
admin.site.register(Message)
admin.site.register(MessageTracker)
