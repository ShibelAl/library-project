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
    This function handles the display and submission of books in the library.

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


@app.route('/edit/<title>', methods=['GET', 'POST'])
def edit_book(title):
    """
    This function handles the editing of a book's details in the library.

    For GET requests, this function retrieves the details of the specified book
    and displays the edit form.

    For POST requests, this function handles the submission of the edited details
    for the specified book. The new details are extracted from the form data and
    used to update the book in the library.

    Form Data (POST request):
        new_title (str): The new title of the book.
        author (str): The new author of the book.
        year (int): The new publication year of the book.
        genre (str): The new genre of the book.

    :argument:
        title (str): The title of the book to be edited.

    :returns:
        - For GET requests: Renders the 'edit_book.html' template with the book's details.
        - For POST requests: Redirects to the 'books' route after updating the book's details.
        - If the book is not found: Redirects to the 'books' route.
    """
    book = next((book for book in library.books if book.title == title), None)
    if not book:
        return redirect(url_for('books'))

    if request.method == 'POST':
        data = request.form
        new_details = {
            "title": data.get('new_title'),
            "author": data.get('author'),
            "publication_year": int(data.get('year')),
            "genre": data.get('genre')
        }
        library.edit_book(title, new_details)
        return redirect(url_for('books'))

    return render_template('edit_book.html', book=book)


@app.route('/delete/<title>')
def delete_book(title):
    """
      This function handles the deletion of a book from the library.

      This function is called when a user navigates to the /delete/<title> route.
      It deletes the specified book from the library based on its title and then
      redirects the user to the list of books.

      :argument:
          title (str): The title of the book to be deleted.

      :returns:
          A redirect response to the 'books' route.
      """
    library.delete_book(title)
    return redirect(url_for('books'))


@app.route('/borrow/<title>')
def borrow_book(title):
    if library.borrow_book(title):
        message = f'You have borrowed "{title}" successfully.'
    else:
        message = f'The book "{title}" is already borrowed or not available.'
    return redirect(url_for('books', message=message))


@app.route('/return/<title>')
def return_book(title):
    if library.return_book(title):
        message = f'You have returned "{title}" successfully.'
    else:
        message = f'The book "{title}" was not borrowed or not available.'
    return redirect(url_for('books', message=message))



if __name__ == '__main__':
    # This will launch the application in debug mode,
    # allowing for automatic code reloads during development.
    app.run(debug=True)