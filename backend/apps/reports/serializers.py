# apps/reports/serializers.py
from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    user_has_liked = serializers.SerializerMethodField()

    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.liked_by.filter(pk=request.user.pk).exists()
        return False

    class Meta:
        model = Report
        fields = ['id', 'user_id', 'content', 'latitude', 'longitude', 'likes', 'user_has_liked', 'created_at']

    def create(self, validated_data):

        request = self.context.get('request')

        # zakladam ze report zna usera
        if request and hasattr(request, "user"):
            validated_data['user'] = request.user

        return super().create(validated_data)