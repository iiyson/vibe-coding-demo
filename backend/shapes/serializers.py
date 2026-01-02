from rest_framework import serializers
from .models import ShapeItem


class ShapeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShapeItem
        fields = ["id", "name", "color", "shape_type", "timestamp"]

