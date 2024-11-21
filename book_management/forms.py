from django import forms

from book_management import models


class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ('name', 'author')
        