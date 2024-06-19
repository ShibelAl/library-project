from flask import Flask, render_template, request, redirect, url_for
from library import Library
from book import Book

# This Flask application serves as the foundation for the library website.

app = Flask(__name__)
library = Library()

@app.route('/')
def index():
    """
    Renders the homepage template

    :returns:
        The rendered HTML content for the homepage.

    :raises:
        TemplateNotFound: If the `index.html` template is not found.
    """

    return render_template('index.html')



@app.route('/books', methods=['GET', 'POST'])
def books():
    """
    Handle the display and submission of books in the library.

    For GET requests, this function retrieves and displays a list of books
    from the library. If provided, it filters the books by the author, genre and the publication year.

    For POST requests, this function handles the submission of a new book
    to the library. The new book's details are extracted from the form data
    and added to the library.

    Form Data (POST):
        title (str): The title of the book.
        author (str): The author of the book.
        year (int): The publication year of the book.
        genre (str): The genre of the book.

    :returns:
        - For GET requests: Renders the 'books.html' template with the list of books.
        - For POST requests: Redirects to the 'books' route after adding the new book.
    """
    if request.method == 'POST':
        data = request.form
        book = Book(data['title'], data['author'], int(data['year']), data['genre'])
        library.add_book(book)
        return redirect(url_for('books'))

    # If I want to see only the books published in the 2008
    # I should put -> publication_year=2008  in the list_books function.
    listed_books = library.list_books()
    return render_template('books.html', books=listed_books)


if __name__ == '__main__':
    # This will launch the application in debug mode,
    # allowing for automatic code reloads during development.
    app.run(debug=True)