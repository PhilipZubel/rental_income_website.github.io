from django.urls import path
from . import views
from .views import TransactionView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static 



urlpatterns = [
    path('', views.TransactionAllView, name='calculator-transactions'),
    path('transactions/<int:pk>/', views.TransactionView.as_view(), name='calculator-transaction'),
    path('transactions/create-transaction/<int:pk>/', views.TransactionCreate.as_view(), name='transaction-create'),
    path('transactions/create-ru/', views.RentalUnitCreate.as_view(), name='rentalunit-create'),
    path('transactions/delete-transaction/<int:pk>/', views.TransactionDelete.as_view(), name='transaction-delete'),
    path('transactions/delete-ru/<int:pk>/', views.RentalUnitDelete.as_view(), name='rentalunit-delete'),

    path('report/<int:year>/', views.Report, name='calculator-report'),
    path('report/<int:year>/<int:pk>/', views.ReportSingleRU, name='calculator-report'),
    ]

if settings.DEBUG:

    #urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
