from django.urls import path
from .views import product_report
from . import views

urlpatterns = [
    path('report/', product_report, name='product_report')
]