from django.urls import path
from myapp.views import ProductListView, Login, Logout, Register


urlpatterns = [
    path('', ProductListView.as_view(), name='product'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
  
]
