from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    comment = serializers.HyperlinkedRelatedField(
        view_name='comment-lists',  # Replace with your comment detail view name
        read_only=True
    )
    
    application = serializers.HyperlinkedRelatedField(
        view_name='application-detail',  # Replace with your application detail view name
        read_only=True
    )

    class Meta:
        model = Notification
        fields = '__all__'

class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        # fields = ['is_read']
        fields = '__all__'