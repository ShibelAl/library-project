class Book:
    def __init__(self, title, author, publication_year, genre):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.genre = genre

    def update(self, title=None, author=None, publication_year=None, genre=None):
        if title:
            self.title = title
        if author:
            self.author = author
        if publication_year:
            self.publication_year = publication_year
        if genre:
            self.genre = genre

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year,
            "genre": self.genre
        }