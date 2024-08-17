import bcrypt
from flask import Blueprint, request, jsonify
from app.models import db, User, Post
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

routes = Blueprint('routes', __name__)

bcrypt = Bcrypt()




@routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'], mobile=data['mobile'], username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401

@routes.route('/create_post', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()
    post = Post(title=data['title'], description=data['description'], tags=data.get('tags'), user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "Post created successfully"}), 201



@routes.route('/publish_post/<int:post_id>', methods=['PATCH'])
@jwt_required()
def publish_post(post_id):
    post = Post.query.get(post_id)
    if post and post.user_id == get_jwt_identity():
        post.is_published = not post.is_published
        db.session.commit()
        return jsonify({"message": "Post status updated"}), 200
    return jsonify({"message": "Post not found or unauthorized"}), 404

@routes.route('/list_posts', methods=['GET'])
@jwt_required()
def list_posts():
    posts = Post.query.filter_by(is_published=True).all()
    return jsonify([{
        "title": post.title,
        "description": post.description,
        "tags": post.tags,
        "likes": post.likes,
        "date": post.created_at.strftime('%d-%m-%Y')
    } for post in posts]), 200

@routes.route('/like_post/<int:post_id>', methods=['PATCH'])
@jwt_required()
def like_post(post_id):
    post = Post.query.get(post_id)
    if post:
        post.likes += 1
        db.session.commit()
        return jsonify({"message": "Post liked"}), 200
    return jsonify({"message": "Post not found"}), 404
