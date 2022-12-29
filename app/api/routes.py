from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Word, word_schema, words_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'hi': 'there'}

# @api.route('/data')
# def viewdata():
#     data = get_word()
#     response = jsonify(data)
#     print(response)
#     return render_template('index.html', data = data)

@api.route('/words', methods = ['POST'])
@token_required
def create_word(current_user_token):
    savedword = request.json['savedword']
    meaning = request.json['meaning']
    speechtype = request.json['speechtype']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    word = Word(savedword, meaning, speechtype, user_token = user_token )

    db.session.add(word)
    db.session.commit()

    response = word_schema.dump(word)
    return jsonify(response)

@api.route('/words', methods = ['GET'])
@token_required
def get_word(current_user_token):
    a_user = current_user_token.token
    words = Word.query.filter_by(user_token = a_user).all()
    response = words_schema.dump(words)
    return jsonify(response)

@api.route('/words/<id>', methods = ['GET'])
@token_required
def get_word_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        word = Word.query.get(id)
        response = word_schema.dump(word)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/words/<id>', methods = ['POST','PUT'])
@token_required
def update_word(current_user_token,id):
    word = Word.query.get(id) 
    word.savedword = request.json['savedword']
    word.meaning = request.json['meaning']
    word.speechtype = request.json['speechtype']
    word.user_token = current_user_token.token

    db.session.commit()
    response = word_schema.dump(word)
    return jsonify(response)


# DELETE word ENDPOINT
@api.route('/words/<id>', methods = ['DELETE'])
@token_required
def delete_word(current_user_token,id):
    word = Word.query.get(id)
    db.session.delete(word)
    db.session.commit()
    response = word_schema.dump(word)
    return jsonify(response)