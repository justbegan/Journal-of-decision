from django_filters import DateRangeFilter, DateFilter
import django_filters
from .models import *
from .forms import *
import django_filters
from django_filters.widgets import RangeWidget


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="decision_date",lookup_expr='gte',label="Дата решения с",widget=DateInput())
    end_date = DateFilter(field_name="decision_date", lookup_expr='lte',label="Дата решения по",widget=DateInput())



    class Meta:
        model = Decision
        fields = ['fio','snils','statement_reg_num','decision_number']

