from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify


class Country(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(
        max_length=2,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"


class Address(models.Model):
    street = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street} {self.postal_code} {self.city}"

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Address Enries"


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    author = models.ForeignKey(
        Author,
        blank=True,
        on_delete=models.CASCADE,
        null=True,
        related_name="books",
    )
    is_bestselling = models.BooleanField(default=False)
    slug = models.SlugField(
        null=False,
        unique=True,
        default="",
        # editable=False,
        blank=True,
        db_index=True,
    )
    published_countries = models.ManyToManyField(
        Country,
        blank=True,
        related_name="books",
    )

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save()

    def __str__(self):
        return f"{self.title} ({self.rating})"

    def get_absolute_url(self):
        return reverse("book-detail", args=[self.slug])
