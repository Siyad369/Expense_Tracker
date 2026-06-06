
from django.urls import path

from .views import *

urlpatterns = [


    path('summary/', SummaryView.as_view()),
    path('reports/', ReportView.as_view()),
    path('calendar/', CalendarView.as_view()),
    path('analytics/category/', CategoryAnalyticsView.as_view()),
    path(
    'analytics/summary/',
    AnalyticsSummaryView.as_view()
    ),

    path(
        'analytics/monthly-trend/',
        MonthlyTrendView.as_view()
    ),

    path(
        'analytics/category-breakdown/',
        ExpenseCategoryBreakdownView.as_view()
    ),
]
