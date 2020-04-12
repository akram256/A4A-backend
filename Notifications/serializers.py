from rest_framework import serializers
from Notifications.models import Notification
from Auth.models import Subscription


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'title', 'body', 'read', 'time_stamp',)
        read_only_fields = ('recipients',)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('email_notifications', 'in_app_notifications')
        read_only_fields = ('user', )