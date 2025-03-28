from django.urls import path
from .views import product_report, product_create_view, product_success
from . import views

urlpatterns = [
    path('report/', product_report, name='product_report'),
    path('product/add/', product_create_view, name='product_add'),
    path('product/success/', product_success, name='product_success'),
]