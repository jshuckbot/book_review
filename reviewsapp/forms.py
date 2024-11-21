from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from reviewsapp.models import Book, Publisher, Review


class SearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.add_input(Submit("", "Search"))

    search = forms.CharField(min_length=3, required=False)
    search_in = forms.ChoiceField(choices=(("title", "Title"), ("contributor", "Contributor")), required=False)


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        exclude = ("date_edited", "book")


class BookMediaForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("cover", "sample")
