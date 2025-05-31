from django.urls import path
from myapp.views import ProductListView, Login, Logout, Register,AdminProductListView,AdminLoginView,CreateProductAdmin,UpdateProductAdmin,RefundProductAdmin,PurchaseList,DeleteProductAdmin


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('admin/product-list/', AdminProductListView.as_view(), name='admin_product_list'),
    path('admin/create-product/',CreateProductAdmin.as_view(), name='admin_create_product'),
    path('admin/update-product/<int:pk>/', UpdateProductAdmin.as_view(), name='admin_update_product'),
    path('admin/refund-product/',RefundProductAdmin.as_view(), name='admin_refund_product'),
    path('purchase_lists', PurchaseList.as_view(), name='purchase_lists'),
    path('admin/product-delete/<int:pk>/', DeleteProductAdmin.as_view(), name='admin_delete_product'),
    
]
