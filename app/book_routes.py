from flask import Blueprint
from app import db
from app.models.book import Book
from flask import jsonify, abort, make_response, request
from sqlalchemy import desc, asc

# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Spin", "A scifi novel set in future Earth."),
#     Book(2, "Where the Wild Things Are", "An illustrated children's book about monsters."),
#     Book(3, "It", "A horror novel about a sadistic clown who terrorizes the residents of Derry, Maine.")
# ] 

# def validate_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         abort(make_response({"message":f"book {book_id} invalid"}, 400))

#     for book in books:
#         if book.id == book_id:
#             return book

#     abort(make_response({"message":f"book {book_id} not found"}, 404))
# 
# books_bp = Blueprint("books", __name__, url_prefix="/books")
# @books_bp.route("", methods=["GET"])
# def handle_books():
#     books_response = []
#     for book in books:
#         books_response.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description
#         })
#     return jsonify(books_response)

# @books_bp.route("/<book_id>", methods=["GET"])
# def handle_book(book_id):
#     book = validate_book(book_id)
#     return {
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description,
#                 }

# ----Helpers----
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

# -------Routes-------
books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book.from_dict(request_body)

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)


@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title")

    if title_query:
        books = Book.query.filter(Book.title.ilike(f"%{title_query}"))
    else:
        books = Book.query.all()
    
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "desc":
            books = Book.query.order_by(desc("title"))
        elif sort_query == "asc":
            books = Book.query.order_by(asc("title"))

    books_response = []

    for book in books:
        books_response.append(book.to_dict())

    return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_model(Book, book_id)
    return book.to_dict()

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()
    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully updated"))

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted"))





