from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import ActivityLog

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return [permissions.AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        ActivityLog.objects.create(
            user=self.request.user,
            action="Create Post",
            details=f"Created post: {post.title}",
        )

    def perform_update(self, serializer):
        post = serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action="Update Post",
            details=f"Updated post: {post.title}",
        )

    def perform_destroy(self, instance):
        ActivityLog.objects.create(
            user=self.request.user,
            action="Delete Post",
            details=f"Deleted post: {instance.title}",
        )
        instance.delete()
