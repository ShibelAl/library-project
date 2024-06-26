import json
import os
import tempfile
import unittest
from library import Library
from book import Book


class TestLibraryClass(unittest.TestCase):

    def clear_library(self):
        """
        Clear the contents of the library (books) and save an empty list to the JSON file.
        """
        self.books = []
        with open("library.json", 'w') as file:
            json.dump([], file)

    def test_library_init_function(self):
        library = Library()
        self.assertEqual(library.filename, "library.json")
        self.assertEqual(library.books, [])

    def test_add_book_function(self):
        library = Library()
        book1 = Book("Sapiens: A Brief History of Humankind",
                     "Yuval Noah Harari", 2011,
                     "Science, History", False, None)
        library.add_book(book1)

        self.assertIn(book1, library.books)
        self.clear_library()

    # to make sure the json file has only [] in it, without any books inside
    def test_list_books_without_filters(self):
        library = Library()
        # book1 is without filters
        book1 = Book("Sapiens", "Yuval", 2011,
                     "Science, History", False, None)
        # book2 is with author filter
        book2 = Book("Sapiens", "Shibel", 2011,
                     "Science, History", False, None)
        # book3 is with author filter
        book3 = Book("Sapiens", "Shibel", 2011,
                     "Science, History", False, None)
        # book4 is with author filter
        book4 = Book("Sapiens", "Bahaa", 2011,
                     "Science, History", False, None)

        # without filter
        library.add_book(book1)
        library.add_book(book2)
        library.add_book(book3)
        library.add_book(book4)
        actual_result = library.list_books()
        expected_list_books = [book1, book2, book3, book4]
        self.assertListEqual(expected_list_books, actual_result)
        self.clear_library()

    def test_list_books_with_filter(self):
        library = Library()
        # book1 is without filters
        book1 = Book("Sapiens", "Shibel", 2011,
                     "Science, History", False, None)
        # book2 is with author filter
        book2 = Book("Sapiens", "Shibel", 2010,
                     "Science, History", False, None)
        # book3 is with author filter
        book3 = Book("Sapiens", "Shibel", 2011,
                     "Science, History", False, None)
        # book4 is with author filter
        book4 = Book("Sapiens", "Bahaa", 2011,
                     "Science, History", False, None)

        # without filter
        library.add_book(book1)
        library.add_book(book2)
        library.add_book(book3)
        library.add_book(book4)
        # the filter here is author and publication_year but can be all the other combinations
        actual_result = library.list_books(author="Shibel", publication_year=2011)
        expected_list_books = [book1, book3]

        self.assertListEqual(expected_list_books, actual_result)
        self.clear_library()

    def test_edit_book_true(self):
        title = "TheTitle"
        new_details = {
            "title": "TheTitle",
            "author": "Shibel",
            "publication_year": 2020,
            "genre": "Action"
        }
        book = Book("TheTitle", "Bahaa", 2000, "Action",
                    False, None)

        library = Library()
        library.add_book(book)

        result = library.edit_book(title, new_details)

        self.assertTrue(result, "Expected edit_book to return True")
        self.clear_library()

    def test_edit_book_false__title_not_found(self):
        title = "TheTitle"
        new_details = {
            "title": "TheTitle",
            "author": "Shibel",
            "publication_year": 2020,
            "genre": "Action"
        }
        book = Book("TheOtherTitle", "Bahaa", 2000, "Action",
                    False, None)

        library = Library()
        library.add_book(book)

        result = library.edit_book(title, new_details)

        self.assertFalse(result, "Expected edit_book to return True")
        self.clear_library()

    def test_edit_book_false__book_is_borrowed(self):
        title = "TheTitle"
        new_details = {
            "title": "TheTitle",
            "author": "Shibel",
            "publication_year": 2020,
            "genre": "Action"
        }
        book = Book("TheTitle", "Bahaa", 2000, "Action",
                    True, None)

        library = Library()
        library.add_book(book)

        result = library.edit_book(title, new_details)

        self.assertFalse(result, "Expected edit_book to return True")
        self.clear_library()

    def test_delete_function(self):
        library = Library()

        # Arrange
        book1 = Book("Sapiens", "Yuval", 2011, "Science, History")
        book2 = Book("21 lessons", "Yuval", 2018, "Social philosophy")

        library.add_book(book1)
        library.add_book(book2)

        library.delete_book(book2.title)
        expected_list = [book1]

        self.assertEqual(expected_list, library.books)
        self.clear_library()

    # need to test the timestamp...
    # def test_borrow_book_true(self):
    #     library = Library()
    #
    #     book1 = Book("Sapiens", "Yuval", 2011, "Science, History",
    #                  True, None)
    #     book2 = Book("21 lessons", "Yuval", 2018, "Social philosophy")
    #     library.add_book(book1)
    #     library.add_book(book2)

    def test_save_library_function(self):
        library = Library()

        book1 = Book("Sapiens", "Yuval", 2011, "Science, History")
        book2 = Book("21 lessons", "Yuval", 2018, "Social philosophy")
        library.add_book(book1)
        library.add_book(book2)

        # Create a temporary file using the tempfile module
        # I don't have access to the library.json, so I created an external temporary file
        # in order to see what happens when I use the save_library function
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_filename = temp_file.name  # for the attribute filename
        temp_file.close()

        library.filename = temp_filename  # In order to save the books in the temporary file

        library.save_library()

        with open(temp_filename, 'r') as file:
            data = json.load(file)
            expected_data = [book1.to_dict(), book2.to_dict()]
            self.assertEqual(data, expected_data)

        # Delete the temporary file
        os.remove(temp_filename)
        self.clear_library()

    def test_load_function(self):
        library = Library()

        book1 = Book("Sapiens", "Yuval", 2011, "Science, History")
        book2 = Book("21 lessons", "Yuval", 2018, "Social philosophy")
        library.add_book(book1)
        library.add_book(book2)

        library.load_library()

        with open("library.json", 'r') as file:
            data = json.load(file)
            self.assertEqual(library.get_books_list(), data)

        self.clear_library()
