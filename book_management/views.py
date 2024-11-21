from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

# from django.views.generic.edit import FormView, UpdateView, CreateView
from django.views.generic import DetailView, DeleteView, FormView, UpdateView, CreateView
from django.views import View
from book_management.forms import BookForm
from book_management.models import Book


class BookRecordFormView(FormView):
    template_name = 'book_form.html'
    form_class = BookForm
    # success_url = '/book_management/entry_success/'
    success_url = reverse_lazy('form_success')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class FormSuccessView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Book record saved successfully")


class DeleteSuccessView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Book record delete successfully")


class BookCreateView(CreateView):
    model = Book
    fields = ('name', 'author')
    template_name = 'book_form.html'
    # success_url = '/book_management/entry_success/'
    success_url = reverse_lazy('form_success')

class BookUpdateView(UpdateView):
    model = Book
    fields = ('name', 'author')
    template_name = 'book_form.html'
    # success_url = '/book_management/entry_success/'
    success_url = reverse_lazy('form_success')



class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book_delete_form.html'
    success_url = '/book_management/delete_success/'
   

class BookDetailView(DeleteView):
    model = Book
    template_name = 'book_detail.html'