from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Projects, CustomUsers, Issues, Comments, Contributors


class CustomUsersAdmin(UserAdmin):
    ordering = ('email', )
    list_filter = ('staff', )

# Register your models here.
admin.site.register(Projects)
#  admin.site.unregister(UserAdmin)
admin.site.register(CustomUsers, CustomUsersAdmin)
admin.site.register(Issues)
admin.site.register(Comments)
admin.site.register(Contributors)
