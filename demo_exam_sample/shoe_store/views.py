from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Users, Products, Providers, Products_in_orders, Orders
from .forms import ProductsForm


def login_view(request):
    if request.method == 'POST':
        user_login = request.POST.get('login')
        user_password = request.POST.get('password')

        try:
            user = Users.objects.get(email=user_login, password=user_password)

            request.session['user_fio'] = f"{user.last_name} {user.first_name} {user.patronymic}"
            # Роль берём из связанной таблицы roles
            request.session['user_role'] = getattr(user.role_id, 'role_name', 'Клиент')

            return redirect('products_list')
        except Users.DoesNotExist:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})

    request.session.flush()
    return render(request, 'login.html')


def products_list(request):
    # Используем имена полей модели: producer, provider, unit, category
    products = Products.objects.select_related('producer', 'provider', 'unit', 'category')

    user_role = request.session.get('user_role')

    # Для гостя — только просмотр без фильтров и сортировок
    if user_role in (None, '', 'Гость'):
        search = None
        sort = None
        provider = None
    else:
        # Поиск по всем текстовым полям товара
        search = request.GET.get('search')
        if search:
            products = products.filter(
                Q(product_name__icontains=search)
                | Q(description__icontains=search)
                | Q(category__category_name__icontains=search)
                | Q(producer__producer_name__icontains=search)
                | Q(provider__provider_name__icontains=search)
            )

        # Сортировка по количеству на складе
        sort = request.GET.get('sort')
        if sort == 'asc':
            products = products.order_by('amount')
        elif sort == 'desc':
            products = products.order_by('-amount')

        # Фильтрация по поставщику
        provider = request.GET.get('provider')
        if provider:
            products = products.filter(provider__id=provider)

    for product in products:
        discount = getattr(product, 'discount', 0) or 0
        product.final_price = int(product.price * (100 - discount) / 100)

    context = {
        'products': products,
        'providers': Providers.objects.all(),
        'user_role': user_role,
    }

    return render(request, 'products.html', context)


def _require_role(request, allowed_roles):
    role = request.session.get('user_role')
    if role not in allowed_roles:
        return redirect('login')
    return None


def product_create(request):
    # Только администратор
    resp = _require_role(request, ['Администратор'])
    if resp:
        return resp

    if request.method == 'POST':
        form = ProductsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductsForm()

    return render(request, 'product_form.html', {'form': form})


def product_update(request, pk):
    # Только администратор
    resp = _require_role(request, ['Администратор'])
    if resp:
        return resp

    product = get_object_or_404(Products, pk=pk)

    if request.method == 'POST':
        form = ProductsForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductsForm(instance=product)

    return render(request, 'product_form.html', {'form': form})


def product_delete(request, pk):
    # Только администратор
    resp = _require_role(request, ['Администратор'])
    if resp:
        return resp

    product = get_object_or_404(Products, pk=pk)

    # Проверка: если товар есть хотя бы в одном заказе — удалять нельзя
    linked = Products_in_orders.objects.filter(product_id=product).exists()

    if request.method == 'POST' and not linked:
        product.delete()
        return redirect('products_list')

    context = {
        'product': product,
        'error': 'Нельзя удалить товар, который присутствует в заказах.' if linked else None,
    }
    return render(request, 'product_confirm_delete.html', context)


def orders_list(request):
    # Менеджер и администратор имеют доступ, остальные видят сообщение
    role = request.session.get('user_role')
    if role not in ['Менеджер', 'Администратор']:
        return render(request, 'orders.html', {
            'orders': [],
            'error': 'Просмотр заказов доступен только менеджеру и администратору.',
        })

    orders = Orders.objects.select_related('pickup_points_id', 'user_id', 'status_id')
    return render(request, 'orders.html', {'orders': orders})
