from django.contrib.auth.models import User
from .models import Product, Delivery, Order
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestShop:

    def test_list_products(self, client):
        response = client.get(reverse('shop:products'))
        assert response.status_code == 200

    def test_product(self, client):
        product = Product.objects.create(name="tea", slug="tea",
                        description="description tea", price=100)

        url = reverse('shop:product', kwargs={'slug': product.slug})
        response = client.get(url)
        assert response.status_code == 200

    def test_order(self, client):
        product = Product.objects.create(name="tea", slug="tea",
                        description="description tea", price=100)
        delivery = Delivery.objects.create(name="Russian Post-Russia",
                    price="1000", delivery_period="5-15 дн.")

        url = reverse('shop:order', kwargs={'slug': product.slug})
        response = client.get(url)
        assert response.status_code == 200

        data = {
            "count_product": 10,
            "name_client": "alexey",
            "phone_client": "+79277817132",
            "adress_client": "ul Mira",
            "delivery": delivery.id,
        }

        response = client.post(url, data)

        orders = Order.objects.all()
        assert 1 == orders.count()
