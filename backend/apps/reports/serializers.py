# apps/reports/serializers.py
from rest_framework import serializers
from .models import Report, AdminComment, StatusChange, UserComment


class UserCommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    is_own = serializers.SerializerMethodField()

    def get_is_own(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author_id == request.user.id
        return False

    class Meta:
        model = UserComment
        fields = ['id', 'author_username', 'text', 'created_at', 'is_own']


class AdminCommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = AdminComment
        fields = ['id', 'author_username', 'text', 'created_at']


class StatusChangeSerializer(serializers.ModelSerializer):
    changed_by_username = serializers.ReadOnlyField(source='changed_by.username')

    class Meta:
        model = StatusChange
        fields = ['old_status', 'new_status', 'changed_by_username', 'changed_at']


class ReportSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    user_has_liked = serializers.SerializerMethodField()
    admin_comments = AdminCommentSerializer(many=True, read_only=True)
    user_comments = UserCommentSerializer(many=True, read_only=True)
    status_history = StatusChangeSerializer(many=True, read_only=True)

    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.liked_by.filter(pk=request.user.pk).exists()
        return False

    class Meta:
        model = Report
        fields = [
            'id', 'user_id', 'content', 'latitude', 'longitude',
            'likes', 'user_has_liked', 'status', 'admin_comments',
            'user_comments', 'status_history', 'created_at',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)


class AdminReportSerializer(serializers.ModelSerializer):
    """Rozszerzony serializer dla widoku admina — zawiera nazwę użytkownika."""
    user_id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    admin_comments = AdminCommentSerializer(many=True, read_only=True)
    status_history = StatusChangeSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = [
            'id', 'user_id', 'username', 'content', 'latitude', 'longitude',
            'likes', 'status', 'admin_comments', 'status_history', 'created_at',
        ]
