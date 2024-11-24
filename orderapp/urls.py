from django.urls import path
from . import views
urlpatterns = [
    path('orders/', views.order_page, name='order_list'),
    path('products/', views.product_page, name='all_products'),
    path('orders/<uuid:order_id>/', views.order_detail, name='order_detail'),
]
