from .forms import ProductForm
from django.contrib.auth.decorators import login_required, permission_required
from .forms import OrderForm
from .models import Product
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Order
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime


@login_required
@permission_required('product.change_order', raise_exception=True)
def change_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status == 'new':
        order.status = 'done'

        # Ustawienie dzisiejszej daty dla pola completion_date
        order.completion_date = datetime.now()

        # Aktualizacja ilości produktu
        product = order.product
        product.quantity += order.quantity
        product.save()

        order.save()

    return redirect(
        'update-order-status')  # Zastąp 'nazwa_widoku_dla_listy_zamówień' odpowiednią nazwą URL.


@login_required
@permission_required('product.view_order', raise_exception=True)
def update_order_status(request):
    # Pobranie wszystkich zamówień o statusie "new"
    new_orders_list = Order.objects.filter(status='new').order_by('-date_ordered')

    return render(request, 'product/update_order_status.html', {'new_orders': new_orders_list})

@login_required
@permission_required('product.view_order', raise_exception=True)
def user_orders(request):
    all_orders = Order.objects.filter(user=request.user).order_by('-date_ordered')

    paginator = Paginator(all_orders, 3)  # Pokaż 3 zamówień na stronie
    page = request.GET.get('page')
    orders = paginator.get_page(page)

    return render(request, 'product/user_orders.html', {'orders': orders})


@login_required
@permission_required('product.add_order', raise_exception=True)
def add_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('user-orders')
    else:
        order_form = OrderForm()

    return render(request, 'product/add_order.html', {'order_form': order_form})



@login_required
@permission_required('product.view_product', raise_exception=True)
def list_products(request):
    product_list = Product.objects.all().order_by('name')
    paginator = Paginator(product_list, 3)  # Pokaż 3 produktów na stronie
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'product/list_products.html', {'products': products})


@login_required
@permission_required('product.add_product', raise_exception=True)  # Zaktualizuj 'your_app_name' do nazwy Twojej aplikacji
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('list-products')  # Zakładam, że posiadasz URL do wyświetlenia listy produktów o nazwie 'list-products'
    else:
        form = ProductForm()

    return render(request, 'product/add_product.html', {'form': form})




