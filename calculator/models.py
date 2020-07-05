from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from partial_date import PartialDateField
from django.urls import reverse

class RentalUnit(models.Model):
	owner = models.ForeignKey(User, on_delete = models.CASCADE)

	RENTAL_TYPES = (
	    ('A','Apartment'),
	    ('G','Garage'),
	    ('H','House'),
	)

	rental_unit_type = models.CharField(max_length=1, choices=RENTAL_TYPES)
	address_city = models.CharField(max_length = 50)
	address_street = models.CharField(max_length = 50)
	address_zip_code = models.CharField(max_length = 10)
	address_number = models.CharField(max_length = 10)

	class Meta:
		ordering = ['address_city','address_street','address_number']
	
	def get_address(self):
		return " ".join([self.address_city, self.address_street, self.address_number])


	def __str__(self):
		return " ".join([self.rental_unit_type+".", self.address_city, self.address_street, self.address_number])

	def get_absolute_url(self):
		return reverse('calculator-transactions')

class Transaction(models.Model):
	rental_unit_id = models.ForeignKey(RentalUnit, on_delete = models.CASCADE)

	TRANSACTION_TYPES = (
		('R','Revenue'),
		('I','Insurance'),
		('P','Property Taxes'),
		('E','Electricity'),
		('A','Administration fees'),
		('O','Other'),
	)

	transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
	transaction_date = models.DateField()
	amount = models.DecimalField(max_digits=10, decimal_places = 2)
	comments = models.CharField(max_length = 1000, null=True)

	
	pdf_file = models.FileField(upload_to="media/",blank=True, null=True)

	def __str__(self):
		return " ".join([str(self.rental_unit_id), self.transaction_type, str(self.transaction_date), str(self.amount)]) 

	def get_absolute_url(self):
		return reverse('calculator-transactions')

