from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView,
    ProductDetailView,
    ContactsPage,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    CategoryListView,
    ProductCategoryList,
)

app_name = CatalogConfig.name


urlpatterns = (
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", ContactsPage.as_view(), name="contacts"),
    path(
        "catalog/<int:pk>/",
        cache_page(60)(ProductDetailView.as_view()),
        name="product_detail",
    ),
    path("catalog/create/", ProductCreateView.as_view(), name="product_create"),
    path("catalog/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path(
        "catalog/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path("catalog/categories/", CategoryListView.as_view(), name="categories"),
    path(
        "catalog/categories/<int:pk>/",
        ProductCategoryList.as_view(),
        name="product_by_category",
    ),
)
