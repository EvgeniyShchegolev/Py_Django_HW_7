import rest_framework.request
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, ValidationError

from advertisements.models import Advertisement
from api_with_restrictions.settings import LIMIT_OPEN_ADVERTISEMENTS


class UserSerializer(ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class AdvertisementSerializer(ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True, )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'draft')
        read_only_fields = ('creator', )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if data.get('status') == 'CLOSED':
            return data

        if data:
            user = self.context['request'].user
            if Advertisement.objects.filter(
                creator=user,
                status='OPEN'
            ).count() >= LIMIT_OPEN_ADVERTISEMENTS:
                raise ValidationError('Превышено количество открытых объявлений')
        return data
