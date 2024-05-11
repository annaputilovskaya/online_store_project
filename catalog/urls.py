from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ContactsPage

app_name = CatalogConfig.name
urlpatterns = (
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsPage.as_view(), name='contacts'),
    path('catalog/<int:pk>/', ProductDetailView.as_view(), name='product_detail')
)
