from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Book
from django.db.models import Avg

# Create your views here.


def index(request):
    books = Book.objects.all().order_by("title")
    context = {
        "books": books,
        "total_number_of_books": books.count(),
        "average_rating": round(books.aggregate(Avg("rating"))["rating__avg"], 2),
    }
    return render(request, "book_outlet/index.html", context)


def book_detail(request, slug):
    # try:
    #     book = Book.objects.get(pk=id)
    # except:
    #     raise Http404()
    book = get_object_or_404(Book, slug=slug)
    context = {
        "title": book.title,
        "author": book.author,
        "rating": book.rating,
        "is_bestseller": book.is_bestselling,
        "published_countries": book.published_countries,
    }
    return render(request, "book_outlet/book_detail.html", context)
