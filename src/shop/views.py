from django.shortcuts import render
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Order
from django.http import Http404
from .forms import OrderForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.views import View


class ProductListView(ListView):
    model = Product
    template_name = "shop/products.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        product_list = Product.objects.all()
        paginator = Paginator(product_list, self.paginate_by)

        page = self.request.GET.get('page', 1)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context['products'] = products
        return context


class ProductView(View):
    template_name = 'shop/product.html'

    def get(self, request, *args, **kwargs):

        if 'slug' in kwargs.keys():
            slug = kwargs['slug']
        else:
            raise Http404("Product does not exist")

        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")

        return render(request, self.template_name, {'product': product},
                        RequestContext(request))


class OrderView(FormView):
    template_name = 'shop/order.html'
    form_class = OrderForm
    success_url = '/shop/order-seccuss'

    def _get_product(self, **kwargs):
        if 'slug' in kwargs.keys():
            slug = kwargs['slug']
        else:
            raise Http404("Page not found")

        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")

        return product

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)

        context['product'] = self._get_product(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, self._get_product(**kwargs))
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form, product):
        order = Order()

        order.count_product = form.cleaned_data['count_product']
        order.delivery = form.cleaned_data['delivery']
        order.name_client = form.cleaned_data['name_client']
        order.phone_client = form.cleaned_data['phone_client']
        order.adress_client = form.cleaned_data['adress_client']
        order.product = product

        order.save()

        return super(OrderView, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['product'] = self._get_product(**kwargs)
        return self.render_to_response(context)


class SuccessOrder(TemplateView):
    template_name = 'shop/success_order.html'
