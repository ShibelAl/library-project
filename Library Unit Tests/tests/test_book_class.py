import unittest
from book import Book
from library import Library

class TestBookClass(unittest.TestCase):

    def test_book_init_function(self):
        book = Book("theTitle", "theAuthor", 2001, "action")
        self.assertEqual(book.title, "theTitle")
        self.assertEqual(book.author, "theAuthor")
        self.assertEqual(book.publication_year, 2001)
        self.assertEqual(book.genre, "action")

    def test_get_title_function(self):
        book = Book("Sapiens", "Yuval", 2011,
                     "Science, History", False, None)

        self.assertEqual(book.get_title(), "Sapiens")

    def test_get_author_function(self):
        book = Book("Sapiens", "Yuval", 2011,
                     "Science, History", False, None)

        self.assertEqual(book.get_author(), "Yuval")

    def test_get_publication_year_function(self):
        book = Book("Sapiens", "Yuval", 2011,
                     "Science, History", False, None)

        self.assertEqual(book.get_publication_year(), 2011)

    def test_get_genre_function(self):
        book = Book("Sapiens", "Yuval", 2011,
                     "Science, History", False, None)

        self.assertEqual(book.get_genre(), "Science, History")

    def test_get_is_borrowed_function(self):
        book = Book("Sapiens", "Yuval", 2011,
                     "Science, History", False, None)

        self.assertEqual(book.get_is_borrowed(), False)

    def test_get_borrowed_timestamp_function(self):
        book = Book("Sapiens", "Yuval", 2011,
                     "Science, History", False, None)

        self.assertEqual(book.get_borrowed_timestamp(), None)

    def test_update_book_function_correct_input(self):
        book = Book("Sapiens", "Yuval", 2011,
                     "Science, History", False, None)

        book.update("sherlock holmes", "shibel", 2001,
                     "mystery")

        self.assertEqual(book.title, "sherlock holmes")
        self.assertNotEqual(book.title, "shibel alshech")

    def test_update_book_function_wrong_input(self):
        book = Book("Sapiens", "Yuval", 2011,
                     "Science, History", False, None)

        book.update("sherlock holmes", "shibel", 2001,
                     "mystery")

        self.assertNotEqual(book.title, "shibel alshech")

    def test_to_dict_function_correct_input(self):

        book = Book("Sapiens", "Yuval", 2011,
                     "Science, History", False, None)


        expected_dict = {"title": "Sapiens", "author": "Yuval", "publication_year": 2011,
                         "genre": "Science, History", "is_borrowed": False,
                         "borrowed_timestamp": None}

        self.assertDictEqual(book.to_dict(), expected_dict)

    def test_to_dict_function_wrong_input(self):

        book = Book("Sapiens", "Yuval", 2011,
                     "Science, History", False, None)

        expected_dict = {"title": "anotherTitle", "author": "Yuval", "publication_year": 2001,
                         "genre": "Science, History", "is_borrowed": False,
                         "borrowed_timestamp": None}
        try:
            self.assertDictEqual(book.to_dict(), expected_dict)
        except AssertionError as e:
            print("Dictionaries do not match. Test Passed")

    def test_borrow_book_function(self):
        book = Book("Sapiens","Yuval", 2011,
                     "Science, History", False, None)

        self.assertTrue(book.borrow())

    def test_return_book__borrowed_book(self):
        book = Book("Sapiens", "Yuval", 2011,
                     "Science, History", True, None)

        self.assertTrue(book.return_book())

    def test_return_book__not_borrowed_book(self):
        book = Book("Sapiens", "Yuval", 2011,
                     "Science, History", False, None)

        self.assertFalse(book.return_book())

    def test_to_dict_function(self):
        book1 = Book("Sapiens: A Brief History of Humankind",
                     "Yuval Noah Harari", 2011,
                     "Science, History", False, None)
