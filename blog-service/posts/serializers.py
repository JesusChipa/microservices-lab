from rest_framework import serializers
from .models import Post
from authors.serializers import AuthorSerializer
from categories.serializers import CategorySerializer


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    excerpt = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'excerpt', 'author', 'category', 'published_at', 'views']
    
    def get_excerpt(self, obj):
        return obj.body[:200] + '...' if len(obj.body) > 200 else obj.body


class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'body', 'author', 'category', 'status', 'published_at', 'views', 'created_at', 'updated_at']
