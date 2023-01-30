import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo import MongoClient

# connect to your database environment variable for your connect
load_dotenv()
mongo_uri = os.environ.get('MONGO_URI')
connect = MongoClient(mongo_uri)

# add in your database and collection from Atlas
database = connect["bookshelf"]
collection = database["books"]

# instantiating new object with "name"
app = Flask(__name__)


# our initial form page
@app.route('/')  # root is "/"
def index():
    return render_template("index.html")


# CREATE
@app.route('/new-book', methods=['POST'])
def add_book():
    # POST new book this is how you'll enter it in Postman
    if request.method == 'POST':
        # request.json returns a JSON object. So you'll see it pretty in Postman
        book = request.json['book']
        pages = request.json['pages']

        # insert new book into books collection in MongoDB
        database['books'].insert_one({"book": book, "pages": pages})

        return "update: Your book has been added to your bookshelf."


# READ
@app.route('/view-books', methods=['GET'])
def view_book():
    if request.method == 'GET':
        # view all books in your mongodb database
        bookshelf = list(database['books'].find())
        titles = []

        # make it pretty
        for books in bookshelf:
            book = books['book']
            pages = books['pages']
            shelf = {'book': book, 'pages': pages}
            # books will go to the top of the list
            titles.insert(0, shelf)
        print(titles)

        return titles


# UPDATE
@app.route('/exchange-book/<string:name>/<int:pages>', methods=['PUT'])  # to update in postman use PUT
def exchange_book(name, pages):
    if request.method == 'PUT':
        new_book = request.json['book']
        new_pages = request.json['pages']

        # this updates your selected book
        database['books'].update_one({"book": name, "pages": pages}, {"$set": {"book": new_book, "pages": new_pages}})

        return "update: Your book has been exchanged."


# DELETE WORKS
@app.route('/remove-book/<string:name>/<int:pages>', methods=['DELETE'])
def remove_book(name, pages):
    if request.method == 'DELETE':
        database['books'].delete_one({"book": name, "pages": pages})

        return "update: Your book has been removed from your bookshelf."
