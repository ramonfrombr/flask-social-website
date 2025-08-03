from datetime import datetime, timezone
from flask import render_template, session, redirect, url_for, current_app

from app.decorators import admin_required, permission_required
from . import main
from .forms import NameForm
from .. import db
from ..models import Permission, User
from ..email import send_email
from flask_login import login_required


@main.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.name.data).first()
    if user is None:
      user = User(username=form.name.data)
      db.session.add(user)
      db.session.commit()
      session['known'] = False
      if current_app.config['APP_ADMIN']:
        send_email(current_app.config['APP_ADMIN'],
                   'New User', 'mail/new_user', user=user)
    else:
      session['known'] = True
    session['name'] = form.name.data
    form.name.data = ''
    return redirect(url_for('.index'))
  return render_template(
      'index.html',
      form=form,
      name=session.get('name'),
      known=session.get('known', False),
      current_time=datetime.now(timezone.utc)
  )


@main.route('/secret')
@login_required
def secret():
  return 'Only authenticated users are allowed!'


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
  return 'For administrators!'


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
  return 'For comment moderators!'


@main.route('/user/<username>')
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('user.html', user=user)
