from datetime import datetime, timezone
from flask import flash, render_template, session, redirect, url_for, current_app

from app.decorators import admin_required, permission_required
from . import main
from .forms import EditProfileForm
from .. import db
from ..models import Permission, User
from ..email import send_email
from flask_login import login_required, current_user


@main.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')


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


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  form = EditProfileForm()
  if form.validate_on_submit():
    current_user.name = form.name.data
    current_user.location = form.location.data
    current_user.about_me = form.about_me.data
    db.session.add(current_user._get_current_object())
    db.session.commit()
    flash('Your profile has been updated.')
    return redirect(url_for('.user', username=current_user.username))
  form.name.data = current_user.name
  form.location.data = current_user.location
  form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', form=form)
