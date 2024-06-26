from datetime import datetime

# ---------------------------
# This class defines the essential characteristics and actions
# of a book in the library management system.
# ---------------------------

class Book:
    def __init__(self, title, author, publication_year, genre, is_borrowed=False, borrowed_timestamp=None):
        """
        Constructor method for the Book class.

        :param title: (str) The title of the book.
        :param author: (str) The author of the book.
        :param publication_year: (int) The year the book was published.
        :param genre: (str) The genre of the book.
        :param borrowed_timestamp: (str, optional) Timestamp when the book was borrowed. Defaults to None.

        Initializes a new instance of the Book class with the given details.
        """

        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.genre = genre
        self.is_borrowed = is_borrowed
        self.borrowed_timestamp = borrowed_timestamp

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_publication_year(self):
        return self.publication_year

    def get_genre(self):
        return self.genre

    def get_is_borrowed(self):
        return self.is_borrowed

    def get_borrowed_timestamp(self):
        return self.borrowed_timestamp

    def update(self, title=None, author=None, publication_year=None, genre=None):
        """
        Updates the attributes of the Book instance.

        :param title: (str, optional) The new title of the book. Defaults to None.
        :param author: (str, optional) The new author of the book. Defaults to None.
        :param publication_year: (int, optional) The new publication year of the book. Defaults to None.
        :param genre: (str, optional) The new genre of the book. Defaults to None.

        Updates the attributes of the Book instance with the new values provided.
        If a parameter is not provided, the corresponding attribute remains unchanged.
        """

        if title:
            self.title = title
        if author:
            self.author = author
        if publication_year:
            self.publication_year = publication_year
        if genre:
            self.genre = genre

    def to_dict(self):
        """
        Converts the Book instance into a dictionary format.

        :returns:
        A dictionary that its keys being the attributes of the Book instance
        (title, author, publication_year, genre), and its values are the
        current values of these attributes.

        This function is Useful for tasks like saving the book information to a file or displaying it in
        a user-friendly format.
        """

        return {
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year,
            "genre": self.genre,
            "is_borrowed": self.is_borrowed,
            "borrowed_timestamp": self.borrowed_timestamp
        }


    def borrow(self):
        """
       Borrow the book.

       :returns: (bool) True if the book was successfully borrowed, False if it was already borrowed.
       """
        if not self.is_borrowed:
            self.is_borrowed = True
            self.borrowed_timestamp = datetime.now().strftime("%d-%m-%Y   %H:%M")
            return True
        return False

    def return_book(self):
        """
        Return the borrowed book.

        :returns:
            bool: True if the book was successfully returned, False if it was not borrowed.
        """
        if self.is_borrowed:
            self.is_borrowed = False
            self.borrowed_timestamp = datetime.now().strftime("%d-%m-%Y   %H:%M")
            return True
        return False
