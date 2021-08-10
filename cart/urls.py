from django.urls import path

from cart.views import cart_detail, success

urlpatterns = [path("cart/", cart_detail, name="cart"), path("success/", success, name="success")]
