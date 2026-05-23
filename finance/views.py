# Create your views here.
from rest_framework import generics
from .models import Category, Transaction, Debt
from .serializers import CategorySerializer, TransactionSerializer, DebtSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .ai_parser import parse_transaction_text

# Category APIs
class CategoryListCreateView(generics.ListCreateAPIView):

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Transaction APIs
class TransactionListCreateView(
    generics.ListCreateAPIView
):

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]

    filterset_fields = ['type', 'category', 'date']
    search_fields = ['note']

    def get_queryset(self):

        return Transaction.objects.filter(
            user=self.request.user
        ).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user
        )


# Debt APIs
class DebtListCreateView(
    generics.ListCreateAPIView
):

    serializer_class = DebtSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        status = self.request.GET.get('status')

        qs = Debt.objects.filter(
            user=self.request.user
        )

        if status:
            qs = qs.filter(status=status)

        return qs.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DebtDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = DebtSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Debt.objects.filter(
            user=self.request.user
        )

class MarkDebtPaidView(APIView):
    def patch(self, request, pk):
        try:
            debt = Debt.objects.get(
                pk=pk,
                user=request.user
            )
            debt.status = 'paid'
            debt.save()
            return Response({"message": "Debt marked as paid"})
        except Debt.DoesNotExist:
            return Response({"error": "Not found"}, status=404)


class AIParseTransactionView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        text = request.data.get("text")

        if not text:
            return Response(
                {"error": "Text required"},
                status=400
            )

        parsed = parse_transaction_text(
            request.user,
            text,
        )

        return Response(parsed)