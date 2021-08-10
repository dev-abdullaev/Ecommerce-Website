from django.urls import path

from items.views import (
    add_product,
    category_list,
    contactView,
    indexView,
    item_delete,
    item_detail,
    item_update,
    searchView,
)

urlpatterns = [
    path("", indexView, name="index"),
    path("search/", searchView, name="search"),
    path("contact/", contactView, name="contact"),
    path("add-item/", add_product, name="add_product"),
    path("detail/<slug:category_slug>/<slug:product_slug>/", item_detail, name="product_detail"),
    path(
        "product-update/<slug:category_slug>/<slug:product_slug>/",
        item_update,
        name="product_update",
    ),
    path(
        "product-delete/<slug:category_slug>/<slug:product_slug>/",
        item_delete,
        name="product_delete",
    ),
    path("cat/<slug:category_slug>/", category_list, name="category_list"),
]
