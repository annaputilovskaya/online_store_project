from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'catalog/contacts.html')
