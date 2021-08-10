import random

from cart.cart import Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, query
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.text import slugify
from django.views.generic import DeleteView, DetailView, UpdateView

from items.forms import AddToCartForm, ItemModelForm
from items.models import Category, Item


def indexView(request):
    newest_products = Item.objects.all()[0:8]
    return render(request, "index.html", {"newest_products": newest_products})


def contactView(request):
    return render(request, "contact.html")


@login_required
def add_product(request):
    if request.method == "POST":
        form = ItemModelForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect("index")
    else:
        form = ItemModelForm()

    context = {"form": form}
    return render(request, "items/product_create.html", context)


def item_detail(request, category_slug, product_slug):
    cart = Cart(request)
    item = get_object_or_404(Item, category__slug=category_slug, slug=product_slug)
    if request.method == "POST":
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            cart.add(product_id=item.id, quantity=quantity, update_quantity=False)

            messages.success(request, "The item has been added to the cart")

            return redirect(
                "product_detail", category_slug=category_slug, product_slug=product_slug
            )
    else:
        form = AddToCartForm()

    related_items = list(item.category.product.exclude(id=item.id))

    if len(related_items) >= 4:
        related_items = random.sample(related_items, 4)

    return render(
        request,
        "items/product_detail.html",
        {"item": item, "form": form, "related_items": related_items},
    )


def item_update(request, category_slug, product_slug):
    item = get_object_or_404(Item, category__slug=category_slug, slug=product_slug)

    if request.method == "POST":
        form = ItemModelForm(request.POST or None, instance=item)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("product_detail", category_slug, product_slug)
    else:
        form = ItemModelForm(instance=item)

    return render(request, "items/product_update.html", {"item": item, "form": form})


def item_delete(request, category_slug, product_slug):
    item = get_object_or_404(Item, category__slug=category_slug, slug=product_slug)
    if request.method == "POST":
        item.delete()
        return redirect("index")

    return render(request, "items/product_delete.html", {"item": item})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return render(request, "items/category_list.html", {"category": category})


def searchView(request):
    query = request.GET.get("query", "")
    items = Item.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    context = {"query": query, "items": items}
    return render(request, "search.html", context)
