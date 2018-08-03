from flask import render_template, session, request, url_for, redirect
from slugify import slugify
from author.decorators import login_required, author_required
import json


from blogapp.app import db
from blog.models import Blog, Post, MainCategory, SubCategory, SubSubCategory, Comment, Reply
from blog.form import PostForm

from flask import Blueprint

admin_app = Blueprint('admin_app', __name__, template_folder='templates')


# main admin route renders dashboard

@admin_app.route("/admin")
@author_required
def admin():

    blog = Blog.query.all()
    comments = Comment.query.filter_by(is_live=False).all()
    replies = Reply.query.filter_by(is_live=False).all()


    if session.get('username'):
        if session.get('is_author') and session.get('is_active'):

            posts = Post.query.order_by(Post.publish_date.desc())
            return render_template('admin/dashboard.html', posts=posts, blog = blog, comments=comments, replies=replies)
        else:
            abort(403)

    else:
        return redirect(url_for('author_app.login'))

@admin_app.route('/moderatecomments', methods=['GET', 'POST'])
def moderatecomments():

    ajaxdata = request.get_json(force=True)

    if ajaxdata["value"] == "approvecomment":
        Comment.approve_comment(ajaxdata["id"])
        return json.dumps({"message": "comment approved"})

    elif ajaxdata["value"] == "deletecomment":
        Comment.delete_comment(ajaxdata["id"])
        return json.dumps({"message": "Comment deleted", "action" : "delete"})

    elif ajaxdata["value"] == "approvereply":
        Reply.approve_reply(ajaxdata["id"])
        return json.dumps({"message": "Reply approved"})
    else:
        Reply.delete_reply(ajaxdata["id"])
        return json.dumps({"message": "Reply deleted", "action" : "delete"})



    return json.dumps({"message": "Error in moderation module"})


@admin_app.route("/post", methods = ['GET', 'POST'])
@author_required
def blogpost():

    blog = Blog.query.all()

    form = PostForm()
    filename = None
    if request.method == 'POST':
        if form.validate_on_submit():
            image = request.files.get('image')
            if image:
                try:
                    filename = uploaded_images.save(image)
                except:
                    flash('The image could not be uploaded')
            else:
                print("File error!")


            maincategory = form.maincategory.data


            if form.new_subcategory.data:
                if not SubCategory.query.filter_by(name=form.new_subcategory.data).first():
                    maincategory.add_subcategory(form.new_subcategory.data, maincategory.id)
                subcategory = SubCategory.query.filter_by(name=form.new_subcategory.data).first()
            elif form.subcategory.data:
                subcategory = form.subcategory.data
            else:
                if(not SubCategory.query.filter_by(name = "No Category")):
                    maincategory.add_subcategory("No Category", maincategory.id)

                subcategory = SubCategory.query.filter_by(name="No Category").first()


            if form.new_subsubcategory.data:
                if not SubSubCategory.query.filter_by(name=form.new_subsubcategory.data).first():
                    subcategory.add_subsubcategory(form.new_subsubcategory.data, subcategory.id)
                subsubcategory = SubSubCategory.query.filter_by(name=form.new_subsubcategory.data).first()

            elif form.subsubcategory.data:
                subsubcategory = form.subsubcategory.data
            else:
                if(not SubSubCategory.query.filter_by(name="No Category").first()):
                    subcategory.add_subsubcategory("No Category", subcategory.id)

                subsubcategory = SubSubCategory.query.filter_by(name="No Category").first()


            blog = Blog.query.first()
            author = Author.query.filter_by(username=session['username']).first()
            title = form.title.data
            body = form.body.data

            slug = slugify(title)
            post = Post(blog, author, title, body, maincategory.id, subcategory.id, subsubcategory.id, filename, slug)

            # Now add the Keywords

            # Extract Keywords from form and add them to Table
            if form.keywords.data:
                keywordstring = form.keywords.data

                # Remove whitespaces and split
                keywords = keywordstring.replace(' ', '').split(",")

                post.add_keywords(keywords)


            db.session.add(post)
            db.session.commit()

            return redirect(url_for('article', slug=slug))



    return render_template("admin/post.html", form=form, action='new', blog=blog)
