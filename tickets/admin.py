from django.contrib import admin
from .models import Ticket, TicketComment

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'created_by', 'assigned_to', 'created_at']
    list_filter = ['status']
    search_fields = ['title', 'description']

@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'author', 'created_at']
