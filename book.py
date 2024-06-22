
# ---------------------------
# This class defines the essential characteristics and actions
# of a book in the library management system.
# ---------------------------
class Book:
    def __init__(self, title, author, publication_year, genre, is_borrowed=False):
        """
        Constructor method for the Book class.

        Parameters:
        title (str): The title of the book.
        author (str): The author of the book.
        publication_year (int): The year the book was published.
        genre (str): The genre of the book.

        Initializes a new instance of the Book class with the given details.
        """

        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.genre = genre
        self.is_borrowed = is_borrowed


    def update(self, title=None, author=None, publication_year=None, genre=None):
        """
        Updates the attributes of the Book instance.

        Parameters:
        title (str, optional): The new title of the book. Defaults to None.
        author (str, optional): The new author of the book. Defaults to None.
        publication_year (int, optional): The new publication year of the book. Defaults to None.
        genre (str, optional): The new genre of the book. Defaults to None.

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

        Returns:
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
            "is_borrowed": self.is_borrowed
        }


    def borrow(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            return True
        return False

    def return_book(self):
        if self.is_borrowed:
            self.is_borrowed = False
            return True
        return False