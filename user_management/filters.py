import django_filters
from .models import Registration

class UsersFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='country', lookup_expr='iexact')

    class Meta:
        model = Registration
        fields = ['country']

class MatchingFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name="country", lookup_expr="iexact")
    address = django_filters.CharFilter(field_name="address", lookup_expr="icontains")

    class Meta:
        model = Registration
        fields = ["country", "address"]