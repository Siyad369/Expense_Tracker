# Create your views here.
from rest_framework import generics
from .models import Category, Transaction, Debt
from .serializers import CategorySerializer, TransactionSerializer, DebtSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response

# Category APIs
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Transaction APIs
class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all().order_by('-date')
    serializer_class = TransactionSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type', 'category', 'date']
    search_fields = ['note']

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


# Debt APIs
class DebtListCreateView(generics.ListCreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    
    def get_queryset(self):
        status = self.request.GET.get('status')
        qs = Debt.objects.all()

        if status:
            qs = qs.filter(status=status)

        return qs.order_by('-created_at')

class DebtDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer

class MarkDebtPaidView(APIView):
    def patch(self, request, pk):
        try:
            debt = Debt.objects.get(pk=pk)
            debt.status = 'paid'
            debt.save()
            return Response({"message": "Debt marked as paid"})
        except Debt.DoesNotExist:
            return Response({"error": "Not found"}, status=404)