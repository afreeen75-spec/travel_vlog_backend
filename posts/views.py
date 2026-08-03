from django.db import models
from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from users.models import ActivityLog

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        queryset = super().get_queryset()
        search = (self.request.query_params.get("search") or "").strip()

        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search)
                | models.Q(description__icontains=search)
                | models.Q(author__username__icontains=search)
            )

        return queryset

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
