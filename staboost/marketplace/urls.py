from django.urls import path
from .views import FetchServicesView, ServiceListView, OrderCreateView

urlpatterns = [
    path('services/fetch/', FetchServicesView.as_view(), name='fetch-services'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
]
