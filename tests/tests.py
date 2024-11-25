import pytest
import tempfile
import os
import shutil
from my_library.library import Library


@pytest.fixture(scope="function")
def temp_db_file():
    """
    Фикстура для создания и удаления временного файла базы данных (JSON)
    """

    temp_dir = tempfile.mkdtemp()
    temp_db_path = os.path.join(temp_dir, "library.json")
    with open(temp_db_path, 'w', encoding='utf-8') as f:
        f.write('[]')
    yield temp_db_path
    shutil.rmtree(temp_dir)


@pytest.fixture
def library(temp_db_file):
    """
    Фикстура для создания экземпляра библиотеки с временной базой данных
    """
    library = Library(temp_db_file)
    return library


def test_add_book(library):
    """
    Тестирование добавления книги
    """
    library.add_book("Test Book", "Test Author", 2024)

    assert len(library.books) == 1
    assert library.books[0].title == "Test Book"
    assert library.books[0].author == "Test Author"
    assert library.books[0].year == 2024


def test_remove_book(library):
    """
    Тестирование удаления книги по ID из тестовой файловой базы данных
    """
    library.add_book("Test Book", "Test Author", 2024)
    book_id = library.books[0].book_id
    library.remove_book(book_id)

    assert len(library.books) == 0


def test_search_books(library):
    """
    Тестирование поиска книги по запросу
    """
    library.add_book("Test Book", "Test Author", 2024)
    library.add_book("Another Book", "Another Author", 2023)

    found_books = library.search_books("Test Book")
    assert len(found_books) == 1
    assert found_books[0].title == "Test Book"

    found_books = library.search_books("Another Author")
    assert len(found_books) == 1
    assert found_books[0].author == "Another Author"

    found_books = library.search_books(2023)
    assert len(found_books) == 1
    assert found_books[0].year == 2023


def test_update_status(library):
    """
    Тестирование изменения статуса книги
    """
    library.add_book("Test Book", "Test Author", 2024)
    book_id = library.books[0].book_id

    library.update_status(book_id, "выдана")
    assert library.books[0].status == "выдана"

    library.update_status(book_id, "неизвестный статус")
    assert library.books[0].status == "выдана"
