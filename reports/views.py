from collections import defaultdict

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

from finance.models import Debt, Transaction


class SummaryView(APIView):
    def get(self, request):
        income = Transaction.objects.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        expense = Transaction.objects.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0

        balance = income - expense

        pending_debt = Debt.objects.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "total_income": income,
            "total_expense": expense,
            "balance": balance,
            "pending_debt": pending_debt
        })
    
class ReportView(APIView):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        transactions = Transaction.objects.all()

        if start_date and end_date:
            transactions = transactions.filter(date__range=[start_date, end_date])

        income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        expense = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "start_date": start_date,
            "end_date": end_date,
            "total_income": income,
            "total_expense": expense,
            "balance": income - expense
        })
    
class CalendarView(APIView):
    def get(self, request):
        transactions = Transaction.objects.all().order_by('date')

        data = defaultdict(list)

        for t in transactions:
            data[str(t.date)].append({
                "id": t.id,
                "type": t.type,
                "amount": t.amount,
                "note": t.note
            })

        return Response(data)

class CategoryAnalyticsView(APIView):
    def get(self, request):
        data = (
            Transaction.objects
            .values('category__name', 'type')
            .annotate(total=Sum('amount'))
        )

        result = []

        for item in data:
            result.append({
                "category": item['category__name'],
                "type": item['type'],
                "total": item['total']
            })

        return Response(result)