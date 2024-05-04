from django.views.generic import ListView, DetailView, TemplateView

from catalog.models import Product, Contacts


# Create your views here.


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ContactsPage(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contacts.objects.get(pk=1)
        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method == 'POST':
            print(request.POST)
            return self.render_to_response(context)
