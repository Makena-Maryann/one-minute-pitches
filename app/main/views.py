from flask import render_template, request, redirect, url_for, abort
from . import main
from ..models import User, Pitch
from .forms import UpdateProfile, PitchForm
from .. import db, photos
from flask_login import login_required, current_user


@main.route('/')
def index():
    pitches = Pitch.query.order_by(Pitch.time.desc()).all()

    return render_template('index.html', pitches=pitches)


@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_pitch():
    form = PitchForm()

    if form.validate_on_submit():
        pitch = Pitch(title=form.title.data, pitch=form.pitch.data,
                      time=Pitch.time, user=current_user)

        db.session.add(pitch)
        db.session.commit()

        return redirect(url_for('.index'))

    return render_template('add.html', pitch_form=form)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))
