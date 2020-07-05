from django.shortcuts import render
from .models import Transaction, RentalUnit
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView, CreateView, DeleteView
from .filters import TransactionFilter
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage


@login_required
def TransactionAllView(request):
	context = {}
	context['rental_units'] = RentalUnit.objects.filter(owner = request.user)
	
	def recursiveTransactionQuerySet(rentals, transaction_set):
		return transaction_set.filter(rental_unit_id__in = context['rental_units'])
		
	context['transactions'] = recursiveTransactionQuerySet(context['rental_units'],Transaction.objects.all().order_by('-transaction_date'))

	myFilter = TransactionFilter(request.GET, queryset=context['transactions'])
	context['myFilter'] = myFilter
	context['transactions'] = myFilter.qs

	
	context['months'] = ['January','Febrary','March','April','May','June','July','August','September','October','November','December']


	return render(request,'calculator/transactions.html',context)

class TransactionView(DetailView):
	model =  RentalUnit
	def get_context_data(self, **kwargs):
		context = {}

		context['rental'] = self.get_object()
		context['rental_units'] = RentalUnit.objects.filter(owner = self.request.user)
			
		context['transactions'] = Transaction.objects.filter(rental_unit_id = context['rental']).order_by('-transaction_date')

		myFilter = TransactionFilter(self.request.GET, queryset=context['transactions'])
		context['myFilter'] = myFilter
		context['transactions'] = myFilter.qs

		context['months'] = ['January','Febrary','March','April','May','June','July','August','September','October','November','December']
		return context

class TransactionCreate(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['transaction_type', 'transaction_date', 'amount', 'comments','pdf_file']

    def form_valid(self, form):
    	form.instance.rental_unit_id = RentalUnit.objects.get(pk=self.kwargs.get('pk'))
    	return super().form_valid(form)

    def get_context_data(self, **kwargs):
    	context = super(TransactionCreate, self).get_context_data(**kwargs)
    	context['rental_units'] = RentalUnit.objects.filter(owner = self.request.user)
    	return context

class TransactionDelete(LoginRequiredMixin, DeleteView):
	model = Transaction
	success_url = reverse_lazy('calculator-transactions')

class RentalUnitCreate(LoginRequiredMixin, CreateView):
    model = RentalUnit
    fields = ['rental_unit_type', 'address_city', 'address_street', 'address_zip_code', 'address_number']

    def form_valid(self, form):
    	form.instance.owner = self.request.user
    	return super().form_valid(form)

    def get_context_data(self, **kwargs):
    	context = super(RentalUnitCreate, self).get_context_data(**kwargs)
    	context['rental_units'] = RentalUnit.objects.filter(owner = self.request.user)
    	return context

class RentalUnitDelete(LoginRequiredMixin, DeleteView):
    model = RentalUnit
    success_url = reverse_lazy('calculator-transactions')

    def test_func(self):
    	ru = self.get_object()
    	if self.user.request == ru.owner:
    		return True
    	return False


@login_required
def DisplayPDF(request, url):
	image_data = open(url, "rb").read()
	return HttpResponse(image_data, mimetype="application/pdf")


# ------------------------------------------- #

@login_required
def Report(request, year):
	context = {'title': "Report"}
	context['rental_units'] = RentalUnit.objects.filter(owner = request.user)
	context["rental_units_count"] = RentalUnit.objects.filter(owner = request.user).count()
	context["this_year"] = year

	def recursiveTransactionQuerySet(rentals, transaction_set):
		return transaction_set.filter(rental_unit_id__in = context['rental_units'])

	transactions = recursiveTransactionQuerySet(context['rental_units'],Transaction.objects.all())
	context["transactions_count"] = transactions.count()
	context["months"] = ["January","February","March","April","May","June","July","August","September","October","November","December"]

	def createlist():
		l = []
		for row in range(12):
			l.append([0.00,0.00,0.00])
		return l

	transactions_years = {year:createlist()}
	transactions_years_total = {year:[0.0,0.0,0.0]}
	years = set()
	total_profit = 0.0
		
	for transaction in transactions:		
		year = transaction.transaction_date.year
		years.add(year)
		month = transaction.transaction_date.month - 1
		if year not in transactions_years.keys():
			transactions_years[year] = createlist()  # total/months, rev/exp/tot
			transactions_years_total[year] = [0.0,0.0,0.0]
		amount = transaction.amount
		trans_type = transaction.transaction_type
		if trans_type == 'R':
			transactions_years[year][month][0] += float(amount)
			transactions_years[year][month][2] += float(amount)
			transactions_years_total[year][0] += float(amount)
			transactions_years_total[year][2] += float(amount)
			total_profit += float(amount)
		else:
			transactions_years[year][month][1] -= float(amount)
			transactions_years[year][month][2] -= float(amount)
			transactions_years_total[year][1] -= float(amount)
			transactions_years_total[year][2] -= float(amount)
			total_profit -= float(amount)

	context['total_profit'] = total_profit
	context['transactions_years_total'] = transactions_years_total
	context['transactions_years'] = transactions_years
	context['years'] = sorted(list(years))[::-1]

	return render(request, 'calculator/report.html', context)

@login_required
def ReportSingleRU(request, year, pk):
	context = {'title': "Report"}
	context['rental_units'] = RentalUnit.objects.filter(owner = request.user)
	context["rental_units_count"] = RentalUnit.objects.filter(owner = request.user).count()
	context['rental'] = RentalUnit.objects.get(pk=pk)
	context["this_year"] = year


	def recursiveTransactionQuerySet(rentals, transaction_set):
		return transaction_set.filter(rental_unit_id__in = context['rental_units'])

	total_transactions_count = recursiveTransactionQuerySet(context['rental_units'],Transaction.objects.all()).count()
	context["transactions_count"] = total_transactions_count

	transactions = Transaction.objects.filter(rental_unit_id = context['rental']).order_by('-transaction_date')
	context["this_transactions_count"] = transactions.count()
	context["months"] = ["January","February","March","April","May","June","July","August","September","October","November","December",]

	def createlist():
		l = []
		for row in range(12):
			l.append([0.0,0.0,0.0])
		return l

	transactions_years = {year:createlist()}
	transactions_years_total = {year:[0.0,0.0,0.0]}
	years = set()
	this_total_profit = 0.0
		
	for transaction in transactions:		
		year = transaction.transaction_date.year
		years.add(year)
		month = transaction.transaction_date.month - 1
		if year not in transactions_years.keys():
			transactions_years[year] = createlist()  # total/months, rev/exp/tot
			transactions_years_total[year] = [0.0,0.0,0.0]
		amount = transaction.amount
		trans_type = transaction.transaction_type
		if trans_type == 'R':
			transactions_years[year][month][0] += float(amount)
			transactions_years[year][month][2] += float(amount)
			transactions_years_total[year][0] += float(amount)
			transactions_years_total[year][2] += float(amount)
			this_total_profit += float(amount)
		else:
			transactions_years[year][month][1] -= float(amount)
			transactions_years[year][month][2] -= float(amount)
			transactions_years_total[year][1] -= float(amount)
			transactions_years_total[year][2] -= float(amount)
			this_total_profit -= float(amount)

	context['this_total_profit'] = this_total_profit
	context['transactions_years_total'] = transactions_years_total
	context['transactions_years'] = transactions_years
	context['years'] = sorted(list(years))[::-1]

	return render(request, 'calculator/report.html', context)