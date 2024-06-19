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
        Initializes a new Library instance.

        Parameters:
        filename (str): The filename to load and save the library data (default is "library.json").
        """

        self.filename = filename
        self.books = []
        self.load_library()

    def add_book(self, book):
        """
        Adds a new book to the library and saves the library data.

        Parameters:
        book (Book): An instance of the Book class to be added to the library.
        """

        self.books.append(book)
        self.save_library()

    def list_books(self, author=None, genre=None, publication_year=None):
        """
        Lists all books in the library or filters them by author and/or genre and/or publication year.

        Parameters:
        author (str, optional): Filter books by the specified author (default is None).
        genre (str, optional): Filter books by the specified genre (default is None).
        publication_year (int, optional): Filter books by the publication_year (default is None).

        :returns:
        list: A list of Book objects that match the specified filter criteria.
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
        Edits the details of an existing book in the library and saves the library data.

        Parameters:
        title (str): The title of the book to be edited.
        new_details (dict): A dictionary containing the updated details of the book.

        :returns:
        bool: True if the book was found and updated successfully, False otherwise.
        """

        for book in self.books:
            if book.title == title:
                book.update(**new_details)
                self.save_library()
                return True
        return False

    def delete_book(self, title):
        """
        Deletes a book from the library and saves the library data.

        Parameters:
        title (str): The title of the book to be deleted.
        """

        self.books = [book for book in self.books if book.title != title]
        self.save_library()

    def save_library(self):
        """
        Saves the current state of the library (list of books) to the JSON file.
        """

        with open(self.filename, 'w') as file:
            json.dump([book.to_dict() for book in self.books], file)

    def load_library(self):
        """
        Loads the library data from the JSON file into the library (list of books).
        If the file does not exist, initializes an empty library.
        """

        try:
            with open(self.filename, 'r') as file:
                book_dicts = json.load(file)
                # The ** operator in Book(**book_dict) unpacks the book_dict
                # dictionary so that each key-value pair is passed as a keyword
                # argument to the Book class constructor.
                self.books = [Book(**book_dict) for book_dict in book_dicts]
        except FileNotFoundError:
            self.books = []