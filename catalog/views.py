from django.shortcuts import render, get_object_or_404

from catalog.models import Product


# Create your views here.


def home(request):
    products = Product.objects.all()
    last_five_products = products.select_related('category').order_by('-created_at')[:5]
    context = {'object_list': last_five_products}
    return render(request, 'catalog/home.html', context=context)


def contacts(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'catalog/contacts.html')


def product_details(request, pk):
    context = {'product': get_object_or_404(Product, pk=pk)}
    return render(request, 'catalog/product_details.html', context=context)
