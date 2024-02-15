from django.contrib import admin
from django.urls import include, path

import reviewsapp.views

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", reviewsapp.views.index),
    path("", include("reviewsapp.urls")),
]
