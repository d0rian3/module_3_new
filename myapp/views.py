from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .models import Product, Purchase, Refund
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView,DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import User
from django.db import transaction
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import ProductForm
from django.db.models import F, ExpressionWrapper, DecimalField
from django.http import HttpResponseForbidden

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class Login(LoginView):
    success_url = '/'
    template_name = 'login.html'
    def get_success_url(self):
        return self.success_url
  

class Register(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/'

class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    login_url = 'login/'
    context_object_name = 'products'
    
    def post(self, request, *args, **kwargs):
        
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id)
        
        if product.count < quantity:
            messages.error(request, f"Не достаточно количества. Только {product.count} предметов доступно.")
            return redirect('product_list')
        
        
        total_cost = product.price * quantity
        if request.user.wallet < total_cost:
            messages.error(request, f"Недостаточно средств. Вам нужно ${total_cost}, но у вас есть только  ${request.user.wallet}")
            return redirect('product_list')
        
        
        with transaction.atomic():
            purchase = Purchase.objects.create(
                user=request.user,
                product=product,
                quantity=quantity
            )
            

            product.count -= quantity
            product.save()
            
            request.user.wallet -= total_cost
            request.user.save()

        
        messages.success(request, f"Успешно оплачено {quantity} x {product.title}")
        return redirect('product_list')
    
class PurchaseList(ListView):
    model = Purchase
    template_name = 'purchase_list.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user).annotate(
            total_price = ExpressionWrapper(F('quantity') * F('product__price'),
                                            output_field=DecimalField(max_digits=20, decimal_places=2)
                                            )
                                            )
    

class AdminLoginView(LoginView):
    template_name = 'admin/admin_login.html'
    redirect_authenticated_user = False
    success_url = '/admin/product-list/'

    def get_success_url(self):
            return '/admin/product-list/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('/admin/product-list/')
            else:
                return HttpResponseForbidden("Доступ только для админов.")
        return super().dispatch(request, *args, **kwargs)
    
class AdminProductListView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = Product
    template_name = 'admin/product_list.html'
    context_object_name = 'products'
    login_url = 'admin-login/'

    def test_func(self):
        return self.request.user.is_superuser
    
class CreateProductAdmin(CreateView):
    model = Product
    template_name = 'admin/create_product.html'
    context_object_name = 'products'
    form_class = ProductForm
    success_url = '/admin/product-list/'


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return self.form_invalid(form)

class UpdateProductAdmin(UpdateView):
    model = Product
    template_name = 'admin/update_product.html'
    context_object_name = 'products'
    success_url = '/admin/product-list/'
    form_class = ProductForm


class RefundProductAdmin(UpdateView):
    model = Product
    template_name = 'admin/refund_list.html'
    context_object_name = 'products'

class DeleteProductAdmin(DeleteView):
    model = Product
    template_name = 'admin/product_list.html'
    success_url = reverse_lazy('admin_product_list')