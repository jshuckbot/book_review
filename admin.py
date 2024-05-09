from django.contrib.admin import AdminSite


class BookAdminSite(AdminSite):
    title_header = "Bookr Admin"
    site_title = "Bookr administration"
    index_title = "Bookr site admin"
    