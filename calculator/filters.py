import django_filters
from django_filters import DateFilter, CharFilter
from .models import RentalUnit


from .models import *

class TransactionFilter(django_filters.FilterSet):
	date_from = DateFilter(field_name = "transaction_date", lookup_expr="gte")
	date_to = DateFilter(field_name = "transaction_date", lookup_expr='lte')
	#rental_unit = RentalUnit.objects.filter(owner = self.request.user)
	class Meta:
		model = Transaction
		fields = []