from flask import Blueprint
from app.books import *
            
books_bp = Blueprint("books", __name__, url_prefix="/books")
@books_bp.route("", methods=["POST"])
def create_book():
    return create_book_implementation()

@books_bp.route("", methods=["GET"])
def read_all_books():
    return read_all_books_implementation()

@books_bp.route("/<book_id>", methods=["GET"])
def handle_book(book_id):
    return handle_book_implementation(book_id)

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    return update_book_implementation(book_id)

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    return delete_book_implementation(book_id)




