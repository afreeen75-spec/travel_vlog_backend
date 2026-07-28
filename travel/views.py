from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import ActivityLog

from .models import Destination
from .serializers import DestinationSerializer


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return [permissions.AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        destination = serializer.save(author=self.request.user)
        ActivityLog.objects.create(
            user=self.request.user,
            action="Create Destination",
            details=f"Created destination: {destination.title}",
        )

    def perform_update(self, serializer):
        destination = serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action="Update Destination",
            details=f"Updated destination: {destination.title}",
        )

    def perform_destroy(self, instance):
        ActivityLog.objects.create(
            user=self.request.user,
            action="Delete Destination",
            details=f"Deleted destination: {instance.title}",
        )
        instance.delete()
