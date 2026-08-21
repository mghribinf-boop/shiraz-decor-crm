from django.db import models

class Customer(models.Model):
    STATUS_CHOICES = [
        ('lead', 'مهتم (Lead)'),
        ('active', 'زبون فعلي (Active)'),
        ('vip', 'زبون مميز (VIP)'),
    ]

    full_name = models.CharField(max_length=150, verbose_name="الاسم الكامل")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lead', verbose_name="حالة الزبون")
    interest = models.CharField(max_length=200, blank=True, null=True, verbose_name="الاهتمامات / المنتجات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    def __str__(self):
        return f"{self.full_name} - {self.phone}"


class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'قيد التجهيز'),
        ('shipping', 'جاري التوصيل'),
        ('delivered', 'تم التسليم'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name="الزبون")
    product_details = models.TextField(verbose_name="تفاصيل الديكور / الطلبية")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ (دج)")
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending', verbose_name="حالة الطلب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")

    def __str__(self):
        return f"طلب #{self.id} - {self.customer.full_name}"