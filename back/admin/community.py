from django.contrib import admin

from back.models.community import Community


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    search_fields = ['name', 'phone', 'email', 'address', 'city', 'owner']
    list_display = ['name', 'phone', 'email', 'address', 'city', 'owner']
