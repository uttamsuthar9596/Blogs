from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'timestamp', 'status')
    list_filter = ('status', 'author')
    search_fields = ('title', 'content')
