import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from .models import Customer, Order
from .forms import CustomerForm, OrderForm

@login_required
def dashboard(request):
    if request.method == 'POST':
        if 'add_customer' in request.POST:
            form = CustomerForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        elif 'add_order' in request.POST:
            form = OrderForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('dashboard')

    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    customers = Customer.objects.all().order_by('-created_at')
    orders = Order.objects.all().order_by('-created_at')

    if search_query:
        customers = customers.filter(
            Q(full_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(interest__icontains=search_query)
        )
        orders = orders.filter(
            Q(product_details__icontains=search_query) |
            Q(customer__full_name__icontains=search_query)
        )

    if status_filter:
        orders = orders.filter(status=status_filter)

    pending_count = Order.objects.filter(status='pending').count()
    shipping_count = Order.objects.filter(status='shipping').count()
    delivered_count = Order.objects.filter(status='delivered').count()

    lead_count = Customer.objects.filter(status='lead').count()
    active_count = Customer.objects.filter(status='active').count()
    vip_count = Customer.objects.filter(status='vip').count()

    context = {
        'customers': customers,
        'orders': orders,
        'total_customers': Customer.objects.count(),
        'total_orders': Order.objects.count(),
        'customer_form': CustomerForm(),
        'order_form': OrderForm(),
        'search_query': search_query,
        'status_filter': status_filter,
        'chart_orders': [pending_count, shipping_count, delivered_count],
        'chart_customers': [lead_count, active_count, vip_count],
    }
    return render(request, 'crm/dashboard.html', context)

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    orders = customer.orders.all().order_by('-created_at')
    total_spent = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': orders.count(),
        'total_spent': total_spent,
    }
    return render(request, 'crm/customer_detail.html', context)

@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('dashboard')

@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('dashboard')

@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'crm/edit_customer.html', {'form': form, 'customer': customer})

@login_required
def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = OrderForm(instance=order)
    return render(request, 'crm/edit_order.html', {'form': form, 'order': order})

@login_required
def invoice_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'crm/invoice.html', {'order': order})

@login_required
def export_customers_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="customers_shiraz_decor.csv"'

    writer = csv.writer(response)
    writer.writerow(['الاسم الكامل', 'رقم الهاتف', 'الحالة', 'الاهتمامات', 'تاريخ الإضافة'])

    customers = Customer.objects.all().values_list('full_name', 'phone', 'status', 'interest', 'created_at')
    for customer in customers:
        writer.writerow(customer)

    return response

@login_required
def export_orders_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="orders_shiraz_decor.csv"'

    writer = csv.writer(response)
    writer.writerow(['رقم الطلب', 'اسم الزبون', 'تفاصيل الطلبية', 'المبلغ (دج)', 'الحالة', 'التاريخ'])

    orders = Order.objects.all()
    for order in orders:
        writer.writerow([order.id, order.customer.full_name, order.product_details, order.total_price, order.get_status_display(), order.created_at])

    return response
    from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa
from .models import Order  # تأكدي من اسم المودل المستعمل للطلبيات

def download_invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template = get_template('crm/invoice_pdf.html')
    html = template.render({'order': order})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response