from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, ProductVersionForm, ProductModeratorForm
from catalog.models import Product, Contacts, ProductVersion, Category
from catalog.services import get_categories_from_cache


class CategoryListView(ListView):
    model = Category

    def get_queryset(self):
        return get_categories_from_cache()


class ProductListView(ListView):
    model = Product
    extra_context = {
        'cat_selected': 0
    }

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('catalog.cancel_publication'):
            return super().get_queryset().order_by('-created_at')
        elif user.is_authenticated:
            return super().get_queryset().filter(Q(owner=user) | Q(is_published=True)).order_by('-created_at')
        return super().get_queryset().filter(is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        products = context_data.get('object_list')
        for product in products:
            versions = ProductVersion.objects.filter(product=product)
            active_versions = versions.filter(is_active=True)
            if active_versions:
                product.active_version = active_versions.last().version_name
            else:
                product.active_version = 'Новый'

        context_data['object_list'] = products
        return context_data


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product = context_data.get('object')
        versions = ProductVersion.objects.filter(product=product)
        active_versions = versions.filter(is_active=True)
        if active_versions:
            product.active_version = active_versions.last().version_name
        else:
            product.active_version = 'Новый'

        context_data['object'] = product
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Product, ProductVersion, form=ProductVersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST)
        else:
            context_data['formset'] = SubjectFormset()
        return context_data

    def form_valid(self, form):
        product = form.save()
        product.owner = self.request.user
        product.save()
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.instance = product
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Product, ProductVersion, form=ProductVersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = SubjectFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        product = form.save()
        if product.owner is None:
            product.owner = self.request.user
            product.save()
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.instance = product
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if (user.has_perm('catalog.change_category')
                and user.has_perm('catalog.change_description')
                and user.has_perm('catalog.cancel_publication')):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')


class ProductCategoryList(ListView):
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    allow_empty = False

    def get_queryset(self):
        user = self.request.user
        result = Product.objects.filter(category=self.kwargs.get('pk')).select_related('category')
        if user.has_perm('catalog.cancel_publication'):
            return result.order_by('-created_at')
        elif user.is_authenticated:
            return result.filter(Q(owner=user) | Q(is_published=True)).order_by('-created_at')
        return result.filter(is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category = context_data['products'][0].category
        context_data['cat_selected'] = category.pk
        products = context_data.get('object_list')
        for product in products:
            versions = ProductVersion.objects.filter(product=product)
            active_versions = versions.filter(is_active=True)
            if active_versions:
                product.active_version = active_versions.last().version_name
            else:
                product.active_version = 'Новый'

        context_data['object_list'] = products
        return context_data


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
