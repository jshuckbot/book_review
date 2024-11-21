from django import template
from reviewsapp.models import Review

register = template.Library()

@register.inclusion_tag('book_list.html')
def book_list(username):
    reviews = Review.objects.filter(creator__username__contains=username)
    book_lists = [review.book.title for review in reviews]
    
    return {'book_read': book_lists}