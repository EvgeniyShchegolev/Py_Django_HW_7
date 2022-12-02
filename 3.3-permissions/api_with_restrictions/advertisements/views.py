import rest_framework.authentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter, FilterSet
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser

from .models import Advertisement
from .serializers import AdvertisementSerializer
from .permission import IsOwnerOrReadOnly
from .filters import AdvertisementFilter


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []

    def list(self, request, *args, **kwargs):

        user = request.user
        if isinstance(user, AnonymousUser):
            serializer = self.get_serializer(self.get_queryset().filter(draft=False), many=True)
        else:
            list_adv = self.get_queryset().filter(Q(creator=user) | Q(draft=False))
            serializer = self.get_serializer(list_adv, many=True)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):

        if request.user == self.get_object().creator or not self.get_object().draft:
            return super().retrieve(request, *args, **kwargs)

        return Response({'details': 'Вы не владелец черновика'})
