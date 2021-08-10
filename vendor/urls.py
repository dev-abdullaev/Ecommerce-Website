from django.urls import path
from order.utilities import notify_customer, notify_vendor

from vendor.views import (adminView, signupView, update_vendor, vendor,
                          vendors_list)

urlpatterns = [
    path("signup/", signupView, name="signup"),
    path("vendor-admin/", adminView, name="admin"),
    path("update-vendor/", update_vendor, name="update_vendor"),
    path("vendors-list/", vendors_list, name="vendors_list"),
    path("<int:vendor_id>/", vendor, name="vendor"),
   
]
