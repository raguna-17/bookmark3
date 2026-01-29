from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    url = models.URLField(max_length=2048)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_favorite = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, through='BookmarkTag', related_name='bookmarks')

    def __str__(self):
        return f"{self.title} ({self.url})"

class BookmarkTag(models.Model):
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("bookmark", "tag")

    def __str__(self):
        return f"{self.bookmark.title} → {self.tag.name}"
