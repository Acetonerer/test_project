from typing import List, Dict
import json
from logger import log, error, success


class Book:
    """
    Класс, собственно, книги
    """
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self) -> str:
        """
        Строковое представление книги

        :return: Строка с данными о книге
        """
        return (f"ID: {self.book_id} "
                f"| Название: {self.title} "
                f"| Автор: {self.author} "
                f"| Год: {self.year} "
                f"| Статус: {self.status}")

    def to_dict(self) -> Dict:
        """
        Преобразует объект книги в словарь

        :return: Словарь с данными книги
        """
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }


class Library:
    """
    Класс, собственно, библиотеки для книг
    """
    def __init__(self, storage_file: str):
        """
        Инициализация библиотеки с загрузкой данных из файла

        :param storage_file: Путь к файлу с данными
        """
        self.storage_file = storage_file
        self.books: List[Book] = self.load_from_database()

    def load_from_database(self) -> List[Book]:
        """
        Метод загрузки данных из БД и преобразования их в объекты класса Book

        :return: Список объектов Book
        """
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                log(f"Загружено {len(data)} книг из базы данных.")
                return [Book(**book_data) for book_data in data]
        except FileNotFoundError:
            log(f"Файл {self.storage_file} не найден. Создается новый пустой список.")
            return []
        except json.JSONDecodeError:
            error(f"Ошибка чтения файла {self.storage_file}. Проверьте его формат.")
            return []

    def save_to_storage(self):
        """
        Метод сохранения данных в БД в формате JSON
        """
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as file:
                json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)
        except Exception as e:
            error(f"Ошибка сохранения данных в файл {self.storage_file}: {e}")

    def add_book(self, title: str, author: str, year: int):
        """
        Метод добавления новой книги в БД

        :param title: Название книги
        :param author: Автор книги
        :param year: Год издания
        """
        next_id = max([book.book_id for book in self.books], default=0) + 1
        new_book = Book(book_id=next_id, title=title, author=author, year=year)
        self.books.append(new_book)
        self.save_to_storage()
        success(f"Книга {new_book} добавлена")

    def remove_book(self, book_id: int):
        """
        Метод удаления книги по её book_id

        :param book_id: ID книги
        """
        book_for_del = next((book for book in self.books if book.book_id == book_id), None)
        if book_for_del:
            self.books.remove(book_for_del)
            self.save_to_storage()
            success(f"Книга с ID {book_id} удалена")
        else:
            error(f"Книга с ID {book_id} не найдена")

    def search_books(self, query: str) -> List[Book]:
        """
        Метод поиска книги в БД по её title, author или year

        :param query: Строка, по которой будет произведен поиск
        :return: Список книг, соответствующих запросу.
        """
        query = str(query).lower()

        found_books = [
            book for book in self.books
            if query in book.title.lower()
            or query in book.author.lower()
            or query == str(book.year)
        ]
        if found_books:
            log(f"Найдено {len(found_books)} книг(и): ")
            for book in found_books:
                log(str(book))
        else:
            error(f"Книг по запросу '{query}' не найдено.")
        return found_books

    def list_books(self) -> List[Book]:
        """
        Метод отображения списка всех книг в БД

        :return: Список объектов Book
        """
        return self.books

    def update_status(self, book_id: int, new_status: str):
        """
        Метод смены статуса книги

        :param book_id: Собственно, ID книги, статус которой нужно изменить
        :param new_status: Новый статус книги
        """
        valid_statuses = {"в наличии", "выдана"}

        if new_status not in valid_statuses:
            error(f"Некорректный статус '{new_status}'. Доступные статусы: {valid_statuses}.")
            return

        book = next((book for book in self.books if book.book_id == book_id), None)

        if book:
            old_status = book.status
            book.status = new_status
            self.save_to_storage()
            success(f"Статус книги '{book.title}' (ID: {book_id}) обновлён с '{old_status}' на '{new_status}'.")
        else:
            error(f"Книга с ID {book_id} не найдена.")
