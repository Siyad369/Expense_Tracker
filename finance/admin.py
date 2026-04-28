from django.contrib import admin

from .models import Category, Debt, Transaction

# Register your models here.
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Debt)
