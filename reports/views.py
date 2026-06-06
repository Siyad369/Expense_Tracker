from collections import defaultdict

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

from finance.models import Debt, Transaction


class SummaryView(APIView):
    def get(self, request):
        income = Transaction.objects.filter(user=request.user, type='income').aggregate(total=Sum('amount'))['total'] or 0
        expense = Transaction.objects.filter(user=request.user,type='expense').aggregate(total=Sum('amount'))['total'] or 0

        balance = income - expense

        pending_debt = Debt.objects.filter(user=request.user, status='pending').aggregate(total=Sum('amount'))['total'] or 0

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

        transactions = Transaction.objects.filter(user=request.user)

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
        transactions = Transaction.objects.filter(user=request.user).order_by('date')

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
            .filter(user=request.user)
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


from datetime import date, timedelta
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response

from finance.models import Transaction

from datetime import date, timedelta
import calendar
class AnalyticsSummaryView(APIView):

    def get(self, request):

        user = request.user

        today = date.today()

        month = int(
            request.GET.get("month", today.month)
        )

        year = int(
            request.GET.get("year", today.year)
        )

        first_day_month = date(
            year,
            month,
            1
        )

        last_day_month = date(
            year,
            month,
            calendar.monthrange(year, month)[1]
        )

        week_start = today - timedelta(days=today.weekday())

        transactions = Transaction.objects.filter(
            user=user
        )

        month_transactions = transactions.filter(
            date__range=[
                first_day_month,
                last_day_month
            ]
        )

        week_transactions = transactions.filter(
            date__gte=week_start
        )

        monthly_income = (
            month_transactions
            .filter(type='income')
            .aggregate(total=Sum('amount'))['total']
            or 0
        )

        monthly_expense = (
            month_transactions
            .filter(type='expense')
            .aggregate(total=Sum('amount'))['total']
            or 0
        )

        weekly_income = (
            week_transactions
            .filter(type='income')
            .aggregate(total=Sum('amount'))['total']
            or 0
        )

        weekly_expense = (
            week_transactions
            .filter(type='expense')
            .aggregate(total=Sum('amount'))['total']
            or 0
        )

        highest_expense_category = (
            transactions
            .filter(type='expense')
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
            .first()
        )

        highest_income_category = (
            transactions
            .filter(type='income')
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
            .first()
        )

        most_expensive_day = (
            transactions
            .filter(type='expense')
            .values('date')
            .annotate(total=Sum('amount'))
            .order_by('-total')
            .first()
        )

        return Response({

            "month": month,
            "year": year,

            "monthly_income": monthly_income,
            "monthly_expense": monthly_expense,

            "weekly_income": weekly_income,
            "weekly_expense": weekly_expense,

            "highest_expense_category":
                highest_expense_category,

            "highest_income_category":
                highest_income_category,

            "most_expensive_day":
                most_expensive_day,

            "total_transactions":
                transactions.count()
        })