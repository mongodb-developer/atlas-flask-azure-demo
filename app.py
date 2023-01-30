import os

import bson
from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo import MongoClient

# Access your MongoDB Atlas cluster
load_dotenv()
mongo_uri = os.environ.get('MONGO_URI')
connection_string = MongoClient(mongo_uri)

# add in your database and collection from Atlas
database = connection_string["bookshelf"]
collection = database["books"]

# instantiating new object with "name"
app = Flask(__name__)

# our initial form page
@app.route('/')  # root is "/"
def index():
    return render_template("index.html")

# CREATE and READ 
@app.route('/books', methods=["GET", "POST"])
def books():
    if request.method == 'POST':
        # CREATE
        book = request.json['book']
        pages = request.json['pages']

        # insert new book into books collection in MongoDB
        collection.insert_one({"book": book, "pages": pages})

        return f"CREATE: Your book {book} ({pages} pages) has been added to your bookshelf.\n "

    elif request.method == 'GET':
        # READ
        bookshelf = list(collection.find())
        novels = []

        for titles in bookshelf:
            book = titles['book']
            pages = titles['pages']
            shelf = {'book': book, 'pages': pages}
            novels.insert(0,shelf)

        return novels
    

# UPDATE
@app.route("/books/<string:book_id>", methods = ['PUT'])
def update_book(book_id: str):
    new_book = request.json['book']
    new_pages = request.json['pages']
    collection.update_one({"_id": bson.ObjectId(book_id)}, {"$set": {"book": new_book, "pages": new_pages}})

    return f"UPDATE: Your book has been updated to: {new_book} ({new_pages} pages).\n"

# DELETE
@app.route("/books/<string:book_id>", methods = ['DELETE'])
def remove_book(book_id: str):
    collection.delete_one({"_id": bson.ObjectId(book_id)})

    return f"DELETE: Your book (id = {book_id}) has been removed from your bookshelf.\n"


