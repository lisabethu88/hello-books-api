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


def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message":f"book {book_id} invalid"}, 400))

    book = Book.query.get(book_id)
    if not book:
        abort(make_response({"message":f"book {book_id} not found"}, 404))

    return book

def create_book_implementation():
    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(f"Book {new_book.title} successfully created", 201)

def read_all_books_implementation():
    # title_query = request.args.get("title")

    # if title_query:
    #     books = Book.query.filter_by(title=title_query)
    # else:
    #     books = Book.query.all()
    
    sort_query = request.args.get("sort")
    dir_query = request.args.get("direction")
    if dir_query == "desc":
        books = Book.query.order_by(desc(sort_query))
    elif dir_query == "asc":
        books = Book.query.order_by(asc(sort_query))

    books_response = []

    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })

    return jsonify(books_response)

def handle_book_implementation(book_id):
    book = validate_book(book_id)

    return {
            "id": book.id,
            "title": book.title,
            "description": book.description
            }

def update_book_implementation(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()
    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return make_response(f"Book #{book.id} successfully updated")

def delete_book_implementation(book_id):
    book = validate_book(book_id)
    db.session.delete(book)
    db.session.commit()

    return make_response(f"Book #{book.id} successfully deleted")


