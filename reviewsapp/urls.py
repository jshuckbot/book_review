from django.urls import path

from reviewsapp import views

urlpatterns = [
    path('', views.index),
    path("books/", views.book_list, name="book_list"),
    # path("book/<int:pk>/", views.book_detail, name="book_detail"),
    path('books/<int:pk>/media/', views.book_media, name='book_media'),
    path('books/<int:book_pk>/reviews/new/', views.review_edit, name='review_create'),
    path('books/<int:book_pk>/reviews/<int:review_pk>/', views.review_edit, name='review_edit'),
    path("books/<int:pk>/", views.BookDetail.as_view(), name="book_detail"),
    path("book-search/", views.book_search, name="book_search"),
    path("publishers/<int:pk>/", views.publisher_edit, name="publisher_edit"),
    path("publishers/new/", views.publisher_edit, name="publiser_create"),

]
