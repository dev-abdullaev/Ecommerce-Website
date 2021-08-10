from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from vendor.models import Vendor


def signupView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            vendor = Vendor.objects.create(name=user.username, created_by=user)

            return redirect("index")
    else:
        form = UserCreationForm()

    context = {"form": form}
    return render(request, "registration/signup.html", context)


@login_required
def adminView(request):
    vendor = request.user.vendor
    products = vendor.product.all()
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    context = {"products": products, "vendor": vendor, "orders": orders}
    return render(request, "vendor/admin.html", context)


@login_required
def update_vendor(request):
    vendor = request.user.vendor

    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")

        if name:
            vendor.created_by.email = email
            vendor.created_by.save()

            vendor.name = name
            vendor.save()

            return redirect("admin")

    return render(request, "vendor/update_vendor.html", {"vendor": vendor})


def vendors_list(request):
    vendors = Vendor.objects.all()

    return render(request, "vendor/vendors_list.html", {"vendors": vendors})


def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    return render(request, "vendor/vendor.html", {"vendor": vendor})
