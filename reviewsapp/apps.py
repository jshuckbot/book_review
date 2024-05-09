from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class ReviewsappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reviewsapp"


class ReviewsappAdminConfig(AdminConfig):
    default_site = 'admin.BookAdminSite'
