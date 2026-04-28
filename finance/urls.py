from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view()),
    
    path('transactions/', TransactionListCreateView.as_view()),
    path('transactions/<int:pk>/', TransactionDetailView.as_view()),

    path('debts/', DebtListCreateView.as_view()),
    path('debts/<int:pk>/', DebtDetailView.as_view()),
    path('debts/<int:pk>/mark-paid/', MarkDebtPaidView.as_view()),


]