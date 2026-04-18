from django.contrib import admin
from .models import Article, Category

admin.site.register(Category)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'views_count', 'created_at']
    list_filter = ['is_published', 'category']
    search_fields = ['title', 'content']
