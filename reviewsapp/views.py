from django.shortcuts import render

from .models import Book, Review
from .utils import average_rating


def book_list(request):
    books = Book.objects.all()
    book_list = []

    for book in books:
        reviews = book.review_set.all()
        book_rating = None
        nuber_of_reviews = 0

        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            nuber_of_reviews = len(reviews)

        book_list.append({"book": book, "book_rating": book_rating, "nuber_of_reviews": nuber_of_reviews})

    context = {"book_list": book_list}

    return render(request, "reviewsapp/books_list.html", context)
