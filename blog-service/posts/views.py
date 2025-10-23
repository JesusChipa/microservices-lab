from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List and retrieve posts.
    
    List supports:
    - Pagination (10 per page)
    - Search (?search=keyword) on title and body
    
    Retrieve is cached for 60 seconds
    """
    queryset = Post.objects.filter(status='published').select_related('author', 'category')
    filter_backends = [SearchFilter]
    search_fields = ['title', 'body']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer
    
    @method_decorator(cache_page(60))
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        # Increment views counter
        post = self.get_object()
        post.views += 1
        post.save(update_fields=['views'])
        return response
