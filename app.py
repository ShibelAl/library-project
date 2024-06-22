from flask import Flask, render_template, request, redirect, url_for, flash
from library import Library
from book import Book
from datetime import datetime

# This Flask application serves as the foundation for the library website.

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # for the flash messages
library = Library()

# Personal Library (List of borrowed books)
personal_library = []


@app.route('/')
def index():
    """
    Renders the index page.

    :return: Rendered HTML of the index page.
    """
    return render_template('index.html')


@app.route('/books')
def books():
    """
    Renders the public library books page, listing all available books with options to borrow or return them.

    :return: Rendered HTML of the public library books page.
    """
    listed_books = library.list_books()
    return render_template('books.html', books=listed_books)


@app.route('/librarians', methods=['GET', 'POST'])
def librarians():
    """
    Renders the librarian's page.
    - If GET request: Display the list of books with options to edit, delete, or add new books.
    - If POST request: Add a new book to the library.

    :return: Rendered HTML of the librarian's page.
    """
    if request.method == 'POST':
        try:
            data = request.form
            new_title = data.get('title')
            author = data.get('author')
            genre = data.get('genre')
            year = data.get('year')

            # Check for empty fields
            if not new_title or not author or not genre or not year:
                raise ValueError('Please fill in all fields.')

            # Convert year to integer
            try:
                publication_year = int(year)
            except ValueError:
                raise ValueError('Invalid year format. Please enter a valid year.')

            # Check if author or genre contain digits
            if any(char.isdigit() for char in author):
                raise ValueError('Author should not contain numbers.')

            if any(char.isdigit() for char in genre):
                raise ValueError('Genre should not contain numbers.')

            # If all checks pass, add the book to the library
            book = Book(new_title, author, publication_year, genre)
            library.add_book(book)
            flash(f'Book "{book.title}" added successfully.', 'success')

        except ValueError as e:
            flash(str(e), 'error')

        return redirect(url_for('librarians'))

    listed_books = library.list_books()
    return render_template('manage_books.html', books=listed_books)

@app.route('/borrow/<title>')
def borrow_book(title):
    """
    Borrow a book from the public library and add it to the personal library.

    :param title: Title of the book to borrow.
    :return: Redirect to the public library books page with a success or error message.
    """
    success, timestamp = library.borrow_book(title)
    if success:
        book = next((book for book in library.books if book.title == title), None)
        if book:
            personal_library.append(book)
        flash(f'Book "{title}" borrowed successfully at {timestamp}.', 'success')
    else:
        flash(f'Book "{title}" could not be borrowed.', 'error')
    return redirect(url_for('books'))


@app.route('/return/<title>')
def return_book(title):
    """
    Return a borrowed book from the personal library to the public library.

    :param title: Title of the book to return.
    :return: Redirect to the public library books page with a success or error message.
    """
    success, timestamp = library.return_book(title)
    if success:
        book = next((book for book in personal_library if book.title == title), None)
        if book:
            personal_library.remove(book)
        flash(f'Book "{title}" returned successfully at {timestamp}.', 'success')
    else:
        flash(f'Book "{title}" could not be returned.', 'error')
    return redirect(url_for('books'))


@app.route('/edit/<title>', methods=['GET', 'POST'])
def edit_book(title):
    """
    Edit the details of an existing book in the library.
    - If GET request: Display the form to edit the book details.
    - If POST request: Update the book details in the library.

    :param title: Title of the book to edit.
    :return: Redirect to the librarian's page with a success or error message.
    """
    book = next((book for book in library.books if book.title == title), None)
    if not book:
        return redirect(url_for('librarians'))

    if request.method == 'POST':
        data = request.form
        try:
            new_year = int(data.get('year'))
        except ValueError:
            flash('Invalid year format. Please enter a valid year.', 'error')
            return redirect(url_for('edit_book', title=title))

        # Check if author or genre contain digits
        if any(char.isdigit() for char in data.get('author', '')):
            flash('Author should not contain numbers.', 'error')
            return redirect(url_for('edit_book', title=title))

        if any(char.isdigit() for char in data.get('genre', '')):
            flash('Genre should not contain numbers.', 'error')
            return redirect(url_for('edit_book', title=title))

        new_details = {
            "title": data.get('new_title'),
            "author": data.get('author'),
            "publication_year": new_year,
            "genre": data.get('genre')
        }

        if new_year > datetime.now().year:
            flash('Publication year cannot be in the future.', 'error')
            return redirect(url_for('edit_book', title=title))

        if library.edit_book(title, new_details):
            flash(f'Book "{title}" updated successfully.', 'success')
        else:
            flash(f'Book "{title}" could not be updated because it is currently borrowed.', 'error')

        return redirect(url_for('librarians'))

    return render_template('edit_book.html', book=book)

@app.route('/delete/<title>')
def delete_book(title):
    """
    Delete a book from the library.

    :param title: Title of the book to delete.
    :return: Redirect to the librarian's page with a success or error message.
    """
    book = next((book for book in library.books if book.title == title), None)
    if book and not book.is_borrowed:
        library.delete_book(title)
        flash(f'Book "{title}" deleted successfully.', 'success')
    else:
        flash(f'Book "{title}" could not be deleted because it is currently borrowed.', 'error')
    return redirect(url_for('librarians'))


@app.route('/personal_library')
def personal_library_view():
    """
    Render the personal library page, listing all borrowed books with options to return them.

    :return: Rendered HTML of the personal library page.
    """
    return render_template('personal_library.html', books=personal_library)


if __name__ == '__main__':
    app.run(debug=True)
