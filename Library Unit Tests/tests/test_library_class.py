import unittest
from library import Library
from book import Book

class testLibraryClass(unittest.TestCase):

    def test_library_init_function(self):
        library = Library()
        self.assertEqual(library.filename, "library.json")

    def test_add_book_function(self):
        library = Library()
        book1 = Book("Sapiens: A Brief History of Humankind",
                     "Yuval Noah Harari", 2011,
                     "Science, History", False, None)
        library.add_book(book1)

        self.assertIn(book1, library.books)

    # def test_list_books_function(self):
