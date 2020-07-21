from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Pitch,Comment
from .forms import UpdateProfile,PitchForm,CommentForm
from .. import db,photos
from flask_login import login_required,current_user
from datetime import datetime

@main.route('/')
def index():
    pitches = Pitch.query.order_by(Pitch.time.desc()).all()

    return render_template('index.html', pitches = pitches)
    
@main.route('/add',methods = ['GET','POST'])
@login_required
def add_pitch():
    form = PitchForm()

    if form.validate_on_submit():
        pitch = Pitch(title = form.title.data, pitch = form.pitch.data,user=current_user)
        
        db.session.add(pitch)
        db.session.commit()

        return redirect(url_for('main.index'))
         
    return render_template('add.html',pitch_form=form)

@main.route('/pitch/<int:id>')
def pitch(id):

    pitch = Pitch.query.filter_by(id=id).first()
    comments = Comment.get_comments(pitch.id)

    return render_template('pitch.html',comments = comments, pitch = pitch)

@main.route('/pitch/comment/new/<int:id>', methods =  ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentForm() 
    pitch = Pitch.query.filter_by(id=id).first()
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comment(pitch_comment=comment,pitch_id = pitch.id,user=current_user) 
        
        new_comment.save_comment()
        
        return redirect(url_for('.pitch',id = pitch.id))

    return render_template('new_comment.html',comment_form=form, pitch=pitch)  

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)    

@main.route('/user/<uname>/update',methods = ['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form=form)

@main.route('/user/<uname>/update/pic',methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
                       
