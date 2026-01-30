from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from .models import Bookmark,Tag
from .serializers import BookmarkSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@login_required
def bookmark_list(request):
    user = request.user

    # 削除処理
    delete_id = request.GET.get("delete")
    if delete_id:
        bm = get_object_or_404(Bookmark, id=delete_id, user=user)
        bm.delete()
        return redirect("bookmark_list")

    # 新規作成 or 更新処理
    if request.method == "POST":
        bm_id = request.POST.get("bookmark_id")
        title = request.POST.get("title")
        url = request.POST.get("url")
        description = request.POST.get("description", "")
        tags_raw = request.POST.get("tags", "")

        tag_names = [t.strip() for t in tags_raw.split(",") if t.strip()]
        tag_objs = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]

        if bm_id:  # 更新
            bm = get_object_or_404(Bookmark, id=bm_id, user=user)
            bm.title = title
            bm.url = url
            bm.description = description
            bm.save()
        else:  # 新規作成
            bm = Bookmark.objects.create(user=user, title=title, url=url, description=description)

        # タグをセット（既存タグは上書き）
        bm.tags.set(tag_objs)

        return redirect("bookmark_list")

    # 一覧取得
    bookmarks = Bookmark.objects.filter(user=user).order_by("-created_at")
    return render(request, "bookmarks.html", {"bookmarks": bookmarks})
