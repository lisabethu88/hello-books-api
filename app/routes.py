from flask import Blueprint, jsonify

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
    Book(1, "Spin", "A scifi novel set in future Earth."),
    Book(2, "Where the Wild Things Are", "An illustrated children's book about monsters."),
    Book(3, "It", "A horror novel about a sadistic clown who terrorizes the residents of Derry, Maine.")
] 

books_bp = Blueprint("books", __name__, url_prefix="/books")
@books_bp.route("", methods=["GET"])
def handle_books():
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET"])
def handle_book(book_id):
    book_id = int(book_id)
    for book in books:
        if book.id == book_id:
            return {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
            