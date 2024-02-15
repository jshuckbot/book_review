from django.contrib import auth
from django.db import models


class Publisher(models.Model):
    """A company that published bools."""

    name = models.CharField(max_length=50, help_text="The name of the publisher")
    website = models.URLField(help_text="The Publisher's website.")
    email = models.EmailField(help_text="The Publisher's email address.")

    def __str__(self):
        return self.name


class Book(models.Model):
    """A publised book."""

    title = models.CharField(max_length=70, help_text="The title of the book.")
    publication_date = models.DateField(verbose_name="Date the book was published.")
    isbn = models.CharField(max_length=20, verbose_name="ISBN number of the book.")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributors = models.ManyToManyField("Contributor", through="BookContributor")

    def __str__(self):
        return self.title


class Contributor(models.Model):
    """A constributor to a Book, e.g. author, editor, co-author"""

    first_names = models.CharField(max_length=50, help_text="The constributor's first name or names.")
    last_names = models.CharField(max_length=50, help_text="The constributor's last name or names.")
    email = models.EmailField(help_text="The contact  email for th constributor")

    def __str__(self):
        return self.first_name


class BookContributor(models.Model):
    class CotributionRole(models.TextChoices):
        AUTHORS = "AUTHORS", "Author"
        CO_AUTHORS = "CO_AUTHORS", "Co_Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(
        verbose_name="The role this contributor had in the book.", choices=CotributionRole.choices, max_length=20
    )


class Review(models.Model):
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(auto_now_add=True, help_text="The data and time the review was created.")
    date_edited = models.DateTimeField(null=True, help_text="The date and time the review was last edited.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="The Book that this review is for.")
