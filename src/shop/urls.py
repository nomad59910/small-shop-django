from django.conf.urls import url
from .views import ProductView, ProductListView, OrderView, SuccessOrder


app_name = 'shop'

urlpatterns = [
    url(r'^products/$', ProductListView.as_view(), name="products"),
    url(r'^product/(?P<slug>[\w-]+)/$', ProductView.as_view(), name="product"),
    url(r'^order-seccuss/$', SuccessOrder.as_view(), name='order-seccuss'),
    url(r'^order/(?P<slug>[\w-]+)/$', OrderView.as_view(), name="order"),
]
