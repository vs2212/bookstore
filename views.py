from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm
from django.core.paginator import Paginator

# Отображение списка книг
def book_list(request):
    books_list = Book.objects.all().order_by('title')  # Сортировка по названию
    paginator = Paginator(books_list, 2)  # 2 элемента на странице
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    return render(request, 'books/book_list.html', {'books': books})

# Отображение деталей книги
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)  # Получаем книгу по её ID
    return render(request, 'books/book_detail.html', {'book': book})

# Добавление новой книги
def book_new(request):
    if request.method == "POST":
        print("Данные формы:", request.POST)  # Отладочный вывод
        form = BookForm(request.POST)
        if form.is_valid():
            print("Форма валидна, сохраняем книгу")  # Отладочный вывод
            form.save()
            return redirect('book_list')
        else:
            print("Форма невалидна:", form.errors)  # Отладочный вывод
    else:
        form = BookForm()
    return render(request, 'books/book_edit.html', {'form': form})

# Редактирование существующей книги
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_edit.html', {'form': form})

# Удаление книги
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')