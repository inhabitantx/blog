from blogapp.app import db

from flask import render_template, redirect, request, url_for, session, flash

from author.form import RegisterForm, LoginForm, ChangePasswordForm
from author.models import Author
from blog.models import Blog
from author.decorators import login_required, author_required, admin_required
import bcrypt


from flask import Blueprint

author_app = Blueprint('author_app', __name__, template_folder='templates')



@author_app.route('/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():

    form = RegisterForm()

    blog = Blog.query.all()

    if request.method == 'POST':
        if form.validate_on_submit():

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf8'), salt)

            fullname = form.fullname.data
            email = form.email.data
            username = form.username.data
            password = hashed_password
            is_author= True
            is_admin= form.is_admin.data
            is_active = True

            author = Author(fullname, email, username, password, is_author, is_admin, is_active)

            db.session.add(author)
            db.session.commit()

            flash('User added successfully')

            return redirect(url_for('admin_app.admin'))

    return render_template('/author/register.html', form=form, blog=blog)

@author_app.route('/delete_user', methods=['GET', 'POST'])
@admin_required
def delete_user():

    blog = Blog.query.all()

    if request.method == 'GET':
        query = Author.query.filter_by(is_active=True).all()

        return render_template('author/delete_user.html', query=query, blog=blog)

    if request.method == 'POST':

        user_id = request.form.get('remove')

        author = Author.query.filter_by(id=user_id).first()

        author.is_active = False

        db.session.add(author)
        db.session.commit()

        flash("Author deleted!")

        return redirect(url_for('admin_app.admin'))

@author_app.route('/change_password', methods=['GET', 'POST'])
@author_required
def change_password():

    form = ChangePasswordForm()

    blog = Blog.query.all()

    if request.method == 'POST':
        if form.validate_on_submit():
            author = Author.query.filter_by(username=session["username"]).first()
            if author:
                check = bcrypt.checkpw(form.oldpassword.data.encode('utf8'), author.password.encode('utf8'))

                if check:
                    salt = bcrypt.gensalt()
                    hashed_password = bcrypt.hashpw(form.newpassword.data.encode('utf8'), salt)
                    author.password = hashed_password
                    db.session.commit()

                    flash("Password updated successfully")
            else:
                flash("Author not found")

    return render_template('author/change_password.html', form=form, blog=blog)



@author_app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    form = LoginForm()

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next')

    if form.validate_on_submit():
        author = Author.query.filter_by(username = form.username.data).first()
        if author:
            if author.is_active:
                check = bcrypt.checkpw(form.password.data.encode('utf8'), author.password.encode('utf8'))
                if check:
                    session['username'] = form.username.data
                    session['is_author'] = author.is_author
                    session['is_admin'] = author.is_admin
                    session['is_active'] = author.is_active
                    if 'next' in session:
                        next = session.get('next')
                        session.pop('next')

                        return redirect(next)
                    else:
                        flash('Logged in')
                        return redirect(url_for('admin_app.admin'))
                else:
                    error = 'Incorrect Username and Password'
            else:
                error = 'Admin Account locked! Contact Site-Admin...'
        else:
            error="Incorrect username or password"
            return render_template('author/login.html', form=form, error=error)


    return render_template('/author/login.html', form=form, error=error)


@author_app.route("/logout")
def logout():
    session.pop('username')
    session.pop('is_author')
    session.pop('is_active')
    flash('Logged out')
    return redirect(url_for('blog_app.index'))
