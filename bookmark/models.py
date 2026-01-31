from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    # タグ名（重複不可）
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        # タグ表示用
        return self.name

# コメント: BookmarkとTagは多対多関係であり、BookmarkTagをthroughとして中間テーブルを明示。
# 中間テーブルを使うことで将来的に追加情報（例: タグ付与日時）を持たせやすい設計。
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    url = models.URLField(max_length=2048)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_favorite = models.BooleanField(default=False)

    # 多対多関係。throughで中間テーブルを指定している点が設計上ポイント
    tags = models.ManyToManyField(Tag, through='BookmarkTag', related_name='bookmarks')

    def __str__(self):
        return f"{self.title} ({self.url})"

class BookmarkTag(models.Model):
    # 中間テーブル。BookmarkとTagの組み合わせをユニークにする
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("bookmark", "tag")

    def __str__(self):
        return f"{self.bookmark.title} → {self.tag.name}"

# レビュー指摘
# - BookmarkTagをthroughにしているのは良い。ただし現在はタグ付与日時などの追加情報は持たせていないので、
#   将来的に拡張可能という意図をコメントに書くと面接で説明しやすい。
# - URLFieldのmax_length2048は妥当だが、フロント入力制限も考慮するとよい。
# - __str__の形式は分かりやすい。面接では「管理画面やログで見やすいように設計した」と説明できる。

