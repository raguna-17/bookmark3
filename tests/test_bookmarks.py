import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from bookmark.models import Bookmark, Tag, BookmarkTag

User = get_user_model()

@pytest.mark.django_db
class TestBookmarkAPI:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username="testuser", password="pass")

    @pytest.fixture
    def auth_client(self, user):
        client = APIClient()
        # トークン取得
        res = client.post("/api/token/", {"username": user.username, "password": "pass"}, format='json')
        access = res.data['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        return client

    def test_create_bookmark(self, auth_client, user):
        data = {
            "title": "テストサイト",
            "url": "https://example.com",
            "description": "テスト用"
        }
        res = auth_client.post("/api/bookmarks/", data, format='json')
        assert res.status_code == 201
        assert Bookmark.objects.filter(title="テストサイト", user=user).exists()

    def test_get_bookmarks(self, auth_client, user):
        Bookmark.objects.create(user=user, title="既存サイト", url="https://exist.com")
        res = auth_client.get("/api/bookmarks/")
        assert res.status_code == 200
        assert any(b["title"] == "既存サイト" for b in res.json())

    def test_update_bookmark(self, auth_client, user):
        bm = Bookmark.objects.create(user=user, title="更新前", url="https://update.com")
        data = {"title": "更新後"}
        res = auth_client.patch(f"/api/bookmarks/{bm.id}/", data, format='json')
        assert res.status_code == 200
        bm.refresh_from_db()
        assert bm.title == "更新後"

    def test_delete_bookmark(self, auth_client, user):
        bm = Bookmark.objects.create(user=user, title="削除対象", url="https://delete.com")
        res = auth_client.delete(f"/api/bookmarks/{bm.id}/")
        assert res.status_code == 204
        assert not Bookmark.objects.filter(id=bm.id).exists()

    def test_unauthenticated_access(self):
        client = APIClient()
        res = client.get("/api/bookmarks/")
        assert res.status_code == 401


@pytest.mark.django_db
def test_tag_str():
    tag = Tag.objects.create(name="Python")
    assert str(tag) == "Python"

@pytest.mark.django_db
def test_bookmark_str():
    user = User.objects.create_user(username="u", password="p")
    bm = Bookmark.objects.create(
        user=user,
        title="Example",
        url="https://example.com"
    )
    assert str(bm) == "Example (https://example.com)"

@pytest.mark.django_db
def test_bookmarktag_str():
    user = User.objects.create_user(username="u2", password="p")
    tag = Tag.objects.create(name="Django")
    bm = Bookmark.objects.create(
        user=user,
        title="Site",
        url="https://site.com"
    )
    bt = BookmarkTag.objects.create(bookmark=bm, tag=tag)
    assert str(bt) == "Site → Django"