from io import BytesIO

from PIL import Image
from django.contrib.auth.decorators import permission_required, user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from django.core.files.images import ImageFile
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views.generic import DetailView

from .forms import SearchForm, PublisherForm, ReviewForm, BookMediaForm
from .models import Book, Review, Contributor, Publisher
from .utils import average_rating
from django.contrib import messages


def index(request):
    return render(request, "base.html")


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


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()

    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {
            "book": book,
            "book_rating": book_rating,
            "reviews": reviews
        }
    else:
        context = {
            "book": book,
            "book_rating": None,
            "reviews": None
        }

    if request.user.is_authenticated:
        max_viewed_books_length = 10
        viewed_books = request.session.get('viewed_books', [])
        viewed_book = [book.id, book.title]
        if viewed_book in viewed_books:
            viewed_books.pop(viewed_books.index(viewed_book))
        viewed_books.insert(0, viewed_book)
        viewed_books = viewed_books[:max_viewed_books_length]
        request.session['viewed_books'] = viewed_books

    return render(request, 'reviewsapp/book_detail.html', context)


def book_search(request):
    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    print(request.GET)
    print(search_text)
    books = set()

    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"

        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        if search_in == "contributor":
            fname_contributors = Contributor.objects.filter(first_names__icontains=search)

            for contributor in fname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

            lname_contributors = Contributor.objects.filter(last_names__icontains=search)

            for contributor in lname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

        if request.user.is_authenticated:
            search_history = request.session.get('search_history', [])
            search_options = [search_in, search]
            if search_options in search_history:
                search_history.pop(search_history.index(search_options))
            search_history.insert(0, search_options)

            request.session['search_history'] = search_history

    return render(request, "reviewsapp/search-results.html",
                  {"form": form, "books": books, "search_text": search_text})


class BookDetail(DetailView):
    template_name = 'reviewsapp/book_detail.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = self.get_object().review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            context['reviews'] = reviews
            context['book_rating'] = book_rating

        else:
            context['reviews'] = None
            context['book_rating'] = None

        if self.request.user.is_authenticated:
            max_viewed_books_length = 10
            viewed_books = self.request.session.get('viewed_books', [])
            viewed_book = [self.object.pk, self.object.title]
            if viewed_book in viewed_books:
                viewed_books.pop(viewed_books.index(viewed_book))
            viewed_books.insert(0, viewed_book)
            viewed_books = viewed_books[:max_viewed_books_length]
            self.request.session['viewed_books'] = viewed_books

        return context


def is_staff_user(user):
    return user.is_staff


@user_passes_test(is_staff_user)
def publisher_edit(request, pk=None):
    publisher = None

    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)

    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, f"Publisher \"{updated_publisher}\" was created")
            else:
                messages.success(request, f"Publisher \"{updated_publisher}\" was updated")

            return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)

    return render(request, "reviewsapp/instance-form.html",
                  {"form": form, "instance": publisher, 'model_type': 'Publisher'})


@login_required
def review_edit(request, book_pk, review_pk=None):
    review = None
    book = get_object_or_404(Book, pk=book_pk)

    if review_pk is not None:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)

        user = request.user
        if not user.is_staff and review.creator.id != user.id:
            raise PermissionDenied

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            update_review = form.save(commit=False)
            update_review.book = book

            if review is None:
                messages.success(request, f"Review for \"{book}\" was created")
            else:
                messages.success(request, f"Review for \"{book}\" was updated")
                update_review.date_edited = now()

            update_review.save()

            return redirect("book_detail", book.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviewsapp/instance-form.html",
                  {
                      "form": form,
                      "instance": review,
                      'model_type': 'Review',
                      "related_instance": book,
                      "related_model_type": "Book"
                  })


@login_required
def book_media(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookMediaForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            cover = form.cleaned_data.get('cover')

            if cover:
                image = Image.open(cover)
                image.thumbnail((300, 300))
                image_data = BytesIO()
                image.save(fp=image_data, format=cover.image.format)
                image_file = ImageFile(image_data)
                book.cover.save(cover.name, image_file)
            book.save()
            messages.success(request, "Book \"{}\" was successfully updated.".format(book))

            return redirect("book_detail", book.pk)
    else:
        form = BookMediaForm(instance=book)

    return render(request, 'reviewsapp/instance-form.html',
                  {"instance": book, "form": form, "model_type": "Book", "is_file_upload": True})
