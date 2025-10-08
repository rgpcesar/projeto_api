import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, make_response
from app import db
from app.models.user_model import User
from app.models.post_model import Post


def init_app(app):

    @app.route('/')
    def index():
        return jsonify({'message': 'Hello, World!'})

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            try:
                data = jwt.decode(
                    token, app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = User.query.get(data['id'])
            except:
                return jsonify({'message': 'Token is invalid!'}), 401
            return f(current_user, *args, **kwargs)
        return decorated

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        token = jwt.encode({
            'id': user.id,
            'exp': (datetime.utcnow() + timedelta(minutes=30)).timestamp()
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing required fields'}), 400

        if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'User already exists'}), 409

        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'New user created!'}), 201

    @app.route('/users', methods=['GET'])
    @token_required
    def get_all_users(current_user):
        users = User.query.all()
        output = []
        for user in users:
            user_data = {}
            user_data['id'] = user.id
            user_data['username'] = user.username
            user_data['email'] = user.email
            output.append(user_data)
        return jsonify({'users': output})

    @app.route('/users/<int:user_id>', methods=['GET'])
    @token_required
    def get_one_user(current_user, user_id):
        user = User.query.get_or_404(user_id)
        user_data = {}
        user_data['id'] = user.id
        user_data['username'] = user.username
        user_data['email'] = user.email
        return jsonify({'user': user_data})

    @app.route('/users/<int:user_id>', methods=['PUT'])
    @token_required
    def update_user(current_user, user_id):
        if current_user.id != user_id:
            return jsonify({'message': 'Cannot perform that function!'}), 403
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        if data.get('password'):
            user.set_password(data['password'])
        db.session.commit()
        return jsonify({'message': 'The user has been updated!'})

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    @token_required
    def delete_user(current_user, user_id):
        if current_user.id != user_id:
            return jsonify({'message': 'Cannot perform that function!'}), 403
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'The user has been deleted!'})

    @app.route('/posts', methods=['POST'])
    @token_required
    def create_post(current_user):
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        if not current_user:
            return jsonify({'message': 'User not found'}), 400
        if 'title' not in data or not data['title']:
            return jsonify({'message': 'Title is required'}), 400
        if not all(char.isalnum() or char.isspace() for char in data['title']):
            return jsonify({'message': 'Title cannot contain special characters'}), 400
        if 'content' not in data or not data['content']:
            return jsonify({'message': 'Content is required'}), 400

        new_post = Post(title=data['title'],
                        content=data['content'], author=current_user)
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'New post created!'}), 201

    @app.route('/posts', methods=['GET'])
    def get_all_posts():
        posts = Post.query.all()
        output = []
        for post in posts:
            post_data = {}
            post_data['id'] = post.id
            post_data['title'] = post.title
            post_data['content'] = post.content
            post_data['date_posted'] = post.date_posted
            post_data['author'] = post.author.username
            output.append(post_data)
        return jsonify({'posts': output})

    @app.route('/posts/<int:post_id>', methods=['GET'])
    def get_one_post(post_id):
        post = Post.query.get_or_404(post_id)
        post_data = {}
        post_data['id'] = post.id
        post_data['title'] = post.title
        post_data['content'] = post.content
        post_data['date_posted'] = post.date_posted
        post_data['author'] = post.author.username
        return jsonify({'post': post_data})

    @app.route('/posts/<int:post_id>', methods=['PUT'])
    @token_required
    def update_post(current_user, post_id):
        post = Post.query.get(post_id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404
        if post.author != current_user:
            return jsonify({'message': 'Cannot perform that function!'}), 403
        data = request.get_json()
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        db.session.commit()
        return jsonify({'message': 'The post has been updated!'})

    @app.route('/posts/<int:post_id>', methods=['DELETE'])
    @token_required
    def delete_post(current_user, post_id):
        post = Post.query.get(post_id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404
        if post.author != current_user:
            return jsonify({'message': 'Cannot perform that function!'}), 403
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'The post has been deleted!'})
