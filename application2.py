from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_store.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80))
    publisher = db.Column(db.String(80))

    def __repr__(self):
        return f"{self.name} - {self.author} - {self.publisher}"

with app.app_context():
    # within this block, current_app points to app.
    print (current_app.name)


@app.route('/')
def index():
    return 'BOOOOKS!'


@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        print(book)
        book_data = {'name': book.name, 'author': book.author, 'publisher': book.publisher}
        print(book_data)
        output.append(book_data)

    return {"books": output}

@app.route('/books/<id>/')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"name": book.name, "author": book.author, "publisher": book.publisher}


@app.route('/books', methods=['POST'])
def add_book():
    book = Book(name=request.json['name'],
                  author=request.json['author'],
                    publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}


@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "yeet!@"}