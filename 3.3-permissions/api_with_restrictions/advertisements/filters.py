from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    date = filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Advertisement
        fields = ['date', 'status', ]
