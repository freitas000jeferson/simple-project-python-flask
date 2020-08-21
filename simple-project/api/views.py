# exemplo
from flask import Flask, jsonify, request, abort, make_response, render_template
from api import app

books = [
    {'id': 1, 'title':'Python Fluente', 'author':'Luciano Ramalho', 'read': False},
    {'id': 2, 'title':'Pense em Python', 'author':'Alberto G. Real', 'read': True},
    {'id': 3, 'title':'Flask Web Framework', 'author':'Whos Who', 'read': False}
]
authors= [
    {'id': 1, 'author':'Luciano Ramalho'},
    {'id': 2, 'author':'Whos Who'},
    {'id': 3, 'author':'Amarantes'},
    {'id': 4, 'author':'Silvio R.'},
    {'id': 5, 'author':'Brunno'},
]

@app.errorhandler(404)
def not_found(error):
    # return  make_response(jsonify({'error': "Not Found"}), 404)
    return jsonify({'error': "Not Found"}), 404


@app.route('/home')
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/api/books', methods=['GET'])
def findAllBooks():
    return jsonify({'books':books})

@app.route('/api/books/<int:book_id>', methods=['GET'])
def findByIdBooks(book_id):
    resp = [b for b in books if b['id'] == book_id]
    if len(resp) > 0:
        return jsonify({'books':resp[0]})
    else:
        abort(404)
    

@app.route("/api/books", methods=["POST"])
def addBook():
    if not request.json or not 'title' in request.json:
        abort(400)
    data= {
        'id': books[-1]['id'] + 1,
        'title': request.json['title'],
        'author': request.json.get('author', ""),
        'read': request.json['read']
    }
    books.append(data)
    return jsonify({"id": data["id"]}), 201


@app.route("/api/books/search")
def searchBook():
    title = request.args["title"]
    resp = [b for b in books if title in b['title']]
    return jsonify({"books": resp, "search": request.args})


@app.route('/api/books/<int:book_id>', methods=['PUT'])
def updateBooks(book_id):
    resp = [b for b in books if b['id'] == book_id]
    if len(resp) > 0:
        books.pop(book_id-1)
        data={
            'id': book_id,
            'title': request.json['title'],
            'author': request.json.get('author', ""),
            'read': request.json['read']
        }
        books.insert(book_id-1, data)
        return jsonify({'books':data}), 200
    else:
        abort(404)
    
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def deleteBooks(book_id):
    resp = [b for b in books if b['id'] == book_id]
    if len(resp) > 0:
        books.remove(resp[0])        
        return jsonify({'remove_books':resp[0]}), 200
    else:
        abort(404)
    


