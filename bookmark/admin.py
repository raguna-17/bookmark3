from django.contrib import admin
from .models import Bookmark, Tag, BookmarkTag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BookmarkTagInline(admin.TabularInline):
    model = BookmarkTag
    extra = 1

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'user', 'is_favorite', 'created_at', 'updated_at')
    list_filter = ('is_favorite', 'created_at', 'updated_at')
    search_fields = ('title', 'url', 'description')
    inlines = [BookmarkTagInline]

@admin.register(BookmarkTag)
class BookmarkTagAdmin(admin.ModelAdmin):
    list_display = ('bookmark', 'tag')
    search_fields = ('bookmark__title', 'tag__name')
