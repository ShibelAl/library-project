import json
from book import Book

# ---------------------------
# This class provides functionality to manage a collection of books,
# including adding, listing, editing, and deleting books, as well as saving
# and loading the library from a JSON file.
# ---------------------------

class Library:
    def __init__(self, filename="library.json"):
        """
        Initialize a Library object.

        :param filename: (str, optional) The filename to load and save library data. Defaults to "library.json".
        """
        self.filename = filename
        self.books = []
        self.load_library()

    def add_book(self, book):
        """
        Add a book to the library and save the updated library data.

        :param book: (Book) The Book object to add to the library.
        """
        self.books.append(book)
        self.save_library()

    def list_books(self, author=None, genre=None, publication_year=None):
        """
        List books in the library, optionally filtering by author, genre, or publication year.

        :param author: (str, optional) Author's name to filter books.
        :param genre: (str, optional) Genre of the books to filter.
        :param publication_year: (int, optional) Year of publication to filter books.

        :returns:
            list: List of Book objects that match the filter criteria.
        """
        filtered_books = self.books
        if author:
            filtered_books = [book for book in filtered_books if book.author == author]
        if genre:
            filtered_books = [book for book in filtered_books if book.genre == genre]
        if publication_year:
            filtered_books = [book for book in filtered_books if book.publication_year == publication_year]
        return filtered_books

    def edit_book(self, title, new_details):

        """
        Edit details of a book in the library, identified by its title.

        :param title: (str) Title of the book to edit.
        :param new_details: (dict) New details to update for the book.

        Returns:
            bool: True if the book was edited successfully, False otherwise.
        """
        for book in self.books:
            if book.title == title:
                if not book.is_borrowed:
                    book.update(**new_details)
                    self.save_library()
                    return True
                else:
                    return False
        return False

    def delete_book(self, title):
        """
        Delete a book from the library by its title.

        :param title: (str) Title of the book to delete.
        """
        self.books = [book for book in self.books if book.title != title]
        self.save_library()

    def borrow_book(self, title):
        """
        Borrow a book from the library, identified by its title.

        :param title: (str) Title of the book to borrow.

        :returns:
            tuple: A tuple where the first element is a boolean indicating if the book was successfully borrowed,
                   and the second element is the timestamp when the book was borrowed (if successful).
        """
        for book in self.books:
            if book.title == title and not book.is_borrowed:
                book.borrow()
                self.save_library()
                return True, book.borrowed_timestamp
        return False, None

    def return_book(self, title):
        """
        This function handles the return of a borrowed book to the library, identified by its title.

        :param title: (str) Title of the book to return.

        :returns:
            tuple: A tuple where the first element is a boolean indicating if the book was successfully returned,
                   and the second element is the timestamp when the book was returned (if successful).
        """
        for book in self.books:
            if book.title == title and book.is_borrowed:
                book.return_book()
                self.save_library()
                return True, book.borrowed_timestamp
        return False, None

    def save_library(self):
        """
        Save the library data to a JSON file.
        """
        with open(self.filename, 'w') as file:
            json.dump([book.to_dict() for book in self.books], file)

    def load_library(self):
        """
        Load the library data from a JSON file.
        """
        try:
            with open(self.filename, 'r') as file:
                book_dicts = json.load(file)
                self.books = [Book(**book_dict) for book_dict in book_dicts]
        except FileNotFoundError:
            self.books = []
