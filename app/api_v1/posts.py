from flask import current_app, g, jsonify, request, url_for
from app.api_v1.decorators import permission_required
from app.api_v1.errors import forbidden
from app.models import Permission, Post
from . import api_v1
from .. import db


@api_v1.route('/posts/')
def get_posts():
  page = request.args.get('page', 1, type=int)
  pagination = Post.query.paginate(
      page=page, per_page=current_app.config['APP_POSTS_PER_PAGE'], error_out=False)
  posts = pagination.items
  prev = None
  if pagination.has_prev:
    prev = url_for('api_v1.get_posts', page=page - 1)
  next = None
  if pagination.has_next:
    next = url_for('api_v1.get_posts', page=page + 1)
  return jsonify({
      'posts': [post.to_json() for post in posts],
      'prev': prev,
      'next': next,
      'count': pagination.total
  })


@api_v1.route('/posts/<int:id>')
def get_post(id):
  post = Post.query.get_or_404(id)
  return jsonify(post.to_json())


@api_v1.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_post():
  post = Post.from_json(request.json)
  post.author = g.current_user
  db.session.add(post)
  db.session.commit()
  return jsonify(post.to_json()), 201, \
      {'Location': url_for('api_v1.get_post', id=post.id)}


@api_v1.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_post(id):
  post = Post.query.get_or_404(id)
  if g.current_user != post.author and \
          not g.current_user.can(Permission.ADMIN):
    return forbidden('Insufficient permissions')
  post.body = request.json.get('body', post.body)
  db.session.add(post)
  db.session.commit()
  return jsonify(post.to_json())
