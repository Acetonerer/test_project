from my_library.library import Library
from my_library.logger import log, error


def main():
    try:
        library = Library("database.json")
        while True:
            log("\nДоступные команды:")
            log("1. Добавить книгу")
            log("2. Удалить книгу")
            log("3. Найти книгу")
            log("4. Показать все книги")
            log("5. Изменить статус книги")
            log("6. Выйти")

            command = input("Введите номер команды: ").strip()

            if command == "1":
                try:
                    title = input("Введите название книги: ").strip()
                    author = input("Введите автора книги: ").strip()
                    year = int(input("Введите год издания: ").strip())
                    library.add_book(title, author, year)
                except ValueError:
                    error("Ошибка: Год издания должен быть числом.")

            elif command == "2":
                try:
                    book_id = int(input("Введите ID книги: ").strip())
                    library.remove_book(book_id)
                except ValueError:
                    error("Ошибка: ID книги должно быть числом.")

            elif command == "3":
                query = input("Введите поисковый запрос (название, автор или год): ").strip()
                library.search_books(query)

            elif command == "4":
                books = library.list_books()
                if books:
                    log("\nСписок книг:")
                    for book in books:
                        log(str(book))
                else:
                    error("Библиотека пуста.")

            elif command == "5":
                try:
                    book_id = int(input("Введите ID книги: ").strip())
                    book = next((book for book in library.books if book.book_id == book_id), None)
                    if not book:
                        error(f"Книга с ID {book_id} не найдена. Попробуйте снова.")
                    else:
                        new_status = input("Введите новый статус ('в наличии' или 'выдана'): ").strip()
                        library.update_status(book_id, new_status)
                except ValueError:
                    error("Ошибка: ID книги должно быть числом.")

            elif command == "6":
                log("Выход из программы. До свидания!")
                break
            else:
                error("Ошибка: Некорректная команда. Попробуйте снова.")

    except KeyboardInterrupt:
        error("\nПрограмма прервана пользователем.")
    except Exception as e:
        error(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()
