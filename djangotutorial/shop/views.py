from django.shortcuts import render, get_object_or_404
from .models import Store, Product
import plotly.express as px
import pandas as pd

def store_list(request):
    stores = Store.objects.all()
    return render(request, 'stores/store_list.html', {'stores': stores})

def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store) # Получаем продукты для конкретного магазина
    return render(request, 'stores/store_detail.html', {'store': store, 'products': products})


def product_report(request):
    products = Product.objects.all()
    data = {
        'Product': [product.name for product in products],
        'Price': [product.price for product in products],
        'Store': [product.store.name for product in products], # Используем store.name для отображения названия магазина
    }
    df = pd.DataFrame(data)

    fig = px.bar(df, x='Product', y='Price', color='Store', title='Product Prices by Store')
    graph = fig.to_html(full_html=False)

    return render(request, 'shop/report.html', {'graph': graph})
