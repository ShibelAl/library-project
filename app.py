from flask import Flask, render_template
from library import Library

# This Flask application serves as the foundation for the library website.

app = Flask(__name__)
library = Library()

@app.route('/')
def index():
    """
    Renders the homepage template

    Returns:
        The rendered HTML content for the homepage.

    Raises:
        TemplateNotFound: If the `index.html` template is not found.
    """

    return render_template('index.html')





if __name__ == '__main__':
    # This will launch the application in debug mode,
    # allowing for automatic code reloads during development.
    app.run(debug=True)