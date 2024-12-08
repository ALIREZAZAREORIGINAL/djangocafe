from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Prodocts, Category
from .forms import SignUpForm
from .forms import SearchForm



def helloworld(request):
    all_prodoct = Prodocts.objects.all()
    all_category = Category.objects.all()
    return render(request, 'index.html', {'prodocts': all_prodoct, 'categories': all_category})


def about(request):
    return render(request, 'about.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "با موفقیت وارد شدید")
            return redirect("home")
        else:
            messages.error(request, "اطلاعات نادرست است!")
            return redirect("login")
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید")
    return redirect("home")


def signup_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ":) حساب کاربری با موفقیت ایجاد شد . خوش آمدید")
            return redirect("home")
        else:
            messages.error(request, 'متاسفانه مشکلی در ثبت نام شما پیش آمده ):')
            return redirect("signup")
    return render(request, 'signup.html', {'form': form})


def product(request, pk):
    product = get_object_or_404(Prodocts, pk=pk)
    return render(request, 'product.html', {'product': product})


def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products_list = Prodocts.objects.filter(category=category)
    paginator = Paginator(products_list, 6)  # نمایش 6 محصول در هر صفحه
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'category_products.html', {'products': products, 'category': category})


def add_to_cart(request, product_id):
    product = get_object_or_404(Prodocts, pk=product_id)
    cart = request.session.get('cart', {})

    if product.QuantityInStock > 0:
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        product.QuantityInStock -= 1
        product.save()
        request.session['cart'] = cart
        messages.success(request, f"محصول {product.Name} با موفقیت به سبد خرید اضافه شد!")
    else:
        messages.error(request, "محصول انتخابی شما در دسترس نیست.")
    
    return redirect('category_products', pk=product.category.id)



def cart(request):
    cart = request.session.get('cart', {})
    products = Prodocts.objects.filter(id__in=cart.keys())
    cart_items = [
        {
            'product': product,
            'quantity': cart[str(product.id)],
            'total_price': product.Price * cart[str(product.id)],
        }
        for product in products
    ]
    total_price = sum(item['total_price'] for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Prodocts, pk=product_id)

    if str(product_id) in cart:
        product.QuantityInStock += cart[str(product_id)]
        del cart[str(product_id)]
        product.save()
    
    request.session['cart'] = cart
    messages.success(request, "محصول از سبد خرید حذف شد.")
    return redirect('cart')


def update_cart(request, product_id):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Prodocts, pk=product_id)
        cart = request.session.get('cart', {})

        if quantity <= product.QuantityInStock + cart.get(str(product_id), 0):
            product.QuantityInStock += cart.get(str(product_id), 0) - quantity
            cart[str(product_id)] = quantity
            product.save()
            request.session['cart'] = cart
            messages.success(request, "سبد خرید بروزرسانی شد.")
        else:
            messages.error(request, "موجودی کافی برای این محصول وجود ندارد.")
    
    return redirect('cart')


def search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Prodocts.objects.filter(Name__icontains=query)

    return render(request, 'search_results.html', {'form': form, 'query': query, 'results': results})


