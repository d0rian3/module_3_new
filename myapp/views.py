from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .models import Product, Purchase, Refund
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User
from django.db import transaction
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import ProductForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    login_url = 'login/'
    context_object_name = 'products'
 
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

