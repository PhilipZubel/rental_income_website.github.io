from django.contrib import admin
from .models import Transaction, RentalUnit

# Register your models here.
admin.site.register(RentalUnit)
admin.site.register(Transaction)
