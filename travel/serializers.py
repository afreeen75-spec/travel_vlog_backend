from rest_framework import serializers

from .models import Destination


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = [
            "id",
            "title",
            "description",
            "country",
            "city",
            "travel_category",
            "attractions",
            "best_season",
            "budget",
            "duration",
            "location",
            "image",
            "created_at",
            "updated_at",
            "author",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "author"]
