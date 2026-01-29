from rest_framework import serializers
from .models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # userは読み取り専用

    class Meta:
        model = Bookmark
        fields = ['id', 'title', 'url', 'description', 'user']  # '__all__' じゃなく明示
