from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='crm/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('customer/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customer/delete/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('customer/edit/<int:pk>/', views.edit_customer, name='edit_customer'),
    path('order/delete/<int:pk>/', views.delete_order, name='delete_order'),
    path('order/edit/<int:pk>/', views.edit_order, name='edit_order'),
    path('order/invoice/<int:pk>/', views.invoice_detail, name='order_invoice'),
    # مسارات التصدير
    path('export/customers/', views.export_customers_csv, name='export_customers'),
    path('export/orders/', views.export_orders_csv, name='export_orders'),
    path('order/<int:order_id>/pdf/', views.download_invoice_pdf, name='download_invoice_pdf'),
]
