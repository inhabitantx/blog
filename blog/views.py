from flask import render_template, redirect, request, url_for, flash, session, abort, jsonify
from slugify import slugify
import bcrypt
import json
from blogapp.app import db


from blog.form import SetupForm, CommentForm, NewsletterForm, PostForm
from blogapp.app import uploaded_images
from author.models import Author
from blog.models import Blog, MainCategory, SubCategory, SubSubCategory, Keywords, Post, Subscribers
from author.decorators import login_required, author_required

from flask import Blueprint

blog_app = Blueprint('blog_app', __name__, template_folder='templates')



POSTS_PER_PAGE = 5

@blog_app.route('/')
@blog_app.route('/index')
def index():

    blog = Blog.query.first()

    if not blog:
        return redirect(url_for('blog_app.setup'))

    latestposts = Post.query.order_by(Post.publish_date.desc()).limit(3)
    maincategories = MainCategory.query.all()

    category1 = maincategories[0].posts.order_by(Post.publish_date.desc()).limit(5).all()
    category2 = maincategories[1].posts.order_by(Post.publish_date.desc()).limit(5).all()
    category3 = maincategories[2].posts.order_by(Post.publish_date.desc()).limit(5).all()

    return render_template('index.html' , latestposts=latestposts, category1=category1, category2=category2, category3=category3)




@blog_app.route('/blog')
@blog_app.route('/blog/<int:page>')
def blog(page=1):

    header = "Blog"
    blog = Blog.query.first()
    categories = MainCategory.query.all()


    if not blog:
        return redirect(url_for('author_app.setup'))

    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)

    return render_template('/blog/blog.html', blog=blog, posts=posts, categories=categories, header=header)

@blog_app.route('/blog/travel')
@blog_app.route('/blog/travel/<int:page>')
def travel(page=1):

    header = "Travel"
    posts = Post.query.filter_by(maincategory_id=1).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    category = MainCategory.query.get(1)

    return render_template('/blog/blog.html', posts=posts, category=category, header=header)

@blog_app.route('/blog/work')
@blog_app.route('/blog/work/<int:page>')
def work(page=1):

    header = "Work"
    posts = Post.query.filter_by(maincategory_id=2).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    category = MainCategory.query.get(2)

    return render_template('/blog/blog.html', posts=posts, category=category, header=header)

@blog_app.route('/blog/photography')
@blog_app.route('/blog/photography/<int:page>')
def photography(page=1):

    header = "Photography"
    posts = Post.query.filter_by(maincategory_id=3).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    category = MainCategory.query.get(3)

    return render_template('/blog/blog.html', posts=posts, category=category, header=header)

@blog_app.route('/search', methods=['GET', 'POST'])
@blog_app.route('/search/<int:page>')
def search(page=1):

    blog = Blog.query.first()

    q = request.form.get('searchbar')

    if q:
        query = Post.query.filter((Post.title.like("%"+ q +"%"))|(Post.body.like("%"+ q +"%"))).all()

        if query:
            return render_template('blog/search.html', posts=query, blog=blog)

    message = "No matching results"
    return render_template('blog/search.html', message=message, blog=blog)



@blog_app.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete():

    """check if argument was provided"""
    query = request.json["query"]
    if not query:
        raise RuntimeError("No argument provided")
    else:
        result = Post.query.filter((Post.title.like("%"+ query +"%"))|(Post.body.like("%"+ query +"%"))|(Post.keywords.like("%"+query+"%"))).all()
        if result:
            allrows = []
            for results in result:
                allrows.append({"title":results.title, "body": results.body[0:70], "img":results.img, "slug":results.slug})


            return json.dumps(allrows)
        else:
            allrows = [{"title": "Results", "img":"cross.png", "body": "No matching results", "slug":"../index"}]

            return json.dumps(allrows)

@blog_app.route('/fetcharticles', methods=['GET', 'POST'])
def fetcharticles():

    """extract keyword from query"""
    keyword = request.json["keyword"]
    if(keyword == 'Recent'):
        articles = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    else:
        maincategoryid = MainCategory.query.filter_by(name=keyword).first().id
        articles = Post.query.filter_by(maincategory_id=maincategoryid).limit(5).all()

    if articles:
        allrows = []
        for article in articles:
            allrows.append({"title":article.title, "body": article.body[0:150], "img":article.img, "slug":article.slug})

        return json.dumps(allrows)
    else:
        allrows = [{"title": "Results", "img":"cross.png", "body": "No matching results", "slug":"../index"}]

        return json.dumps(allrows)


@blog_app.route('/about')
def about():
    return render_template('about.html')

@blog_app.route('/contact')
def contact():
    return render_template('contact.html')




@blog_app.route("/setup", methods=['GET', 'POST'])
def setup():
    error = None

    form = SetupForm()
    blog = Blog.query.first()

    if request.method == 'GET':

        if blog:
            return redirect(url_for('index'))
        else:

            return render_template("/blog/setup.html", form=form)

    if not blog and request.method == 'POST':
        if form.validate_on_submit():
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf8'), salt)
            author = Author(
                form.fullname.data,
                form.email.data,
                form.username.data,
                hashed_password,
                True,
                True,
                True
                )
            db.session.add(author)
            db.session.flush()


            if author.id:
                blog = Blog(
                form.title.data,
                author.id
                )
                db.session.add(blog)
                db.session.flush()
            else:
                db.session.rollback()
                error = "Error creating new Entry"

            if blog.id:
                maincategories = [MainCategory(form.category1.data),
                                    MainCategory(form.category2.data),
                                    MainCategory(form.category3.data)]

                db.session.add_all(maincategories)
                db.session.flush()

            if author.id and blog.id:
                db.session.commit()
                session['username'] = form.username.data
                session['is_author'] = author.is_author
                session['is_admin'] = author.is_admin
                session['is_active'] = author.is_active
                flash("Blog created successfully")
                return redirect(url_for('admin_app.admin'))
            else:
                db.session.rollback()
                error = "Error creating new Blog"

    return render_template('/blog/setup.html', form = form, error=error, blog=blog)





@blog_app.route("/article/<slug>")
def article(slug):

    form = CommentForm()

    post = Post.query.filter_by(slug=slug).first_or_404()
    replies = post.reply.filter_by(is_live=True).all()
    comments = post.comment.filter_by(is_live=True).all()

    return render_template('/blog/article.html', post = post, comments = comments, form = form, replies=replies)

@blog_app.route("/edit/<int:post_id>", methods=['GET', 'POST'])
def edit(post_id):

    post = Post.query.filter_by(id=post_id).first_or_404()

    blog = Blog.query.all()

    form = PostForm(obj=post)

    if form.validate_on_submit():
        original_image = post.img
        # form.populate_obj(post)
        if form.image.has_file():
            image = request.files.get('image')
            try:
                filename = uploaded_images.save(image)
            except:
                flash('Image could not be uploded')
            if filename:
                post.img = filename
        else:
            post.img = original_image

        if(form.maincategory.data):
            post.maincategory_id = (form.maincategory.data).id
        if(form.subcategory.data):
            post.subcategory_id = (form.subcategory.data).id
        if(form.subsubcategory.data):
            post.subsubcategory_id = (form.subsubcategory.data).id

        if form.new_subcategory.data:
            maincategory.add_subcategory(form.new_subcategory.data, maincategory.id)
            subcategory = SubCategory.query.filter_by(name=form.new_subcategory.data)
            post.subcategory = subcategory.id

        if form.new_subsubcategory.data:
            subcategory.add_subsubcategory(form.new_subsubcategory.data, subcategory.id)
            subsubcategory = SubSubCategory.query.filter_by(name=form.new_subsubcategory.data).first()
            post.subsubcategory = subsubcategory.id


        db.session.commit()
        return redirect(url_for('.article', slug = post.slug))

    return render_template('/admin/post.html', form=form, post=post, action='edit', blog=blog)


@blog_app.route("/delete/<int:post_id>")
@author_required
def delete(post_id):
    post = Post.query.filter_by(id = post_id).first_or_404()

    post.live = False

    db.session.add(post)
    db.session.commit()

    flash('Article deleted!')

    return redirect('/admin')


@blog_app.route('/addsubscriber', methods=['GET', 'POST'])
def addsubscriber():

    subscriber = request.get_json(force=True)

    is_in_list = Subscribers.query.filter_by(email=subscriber["email"]).first()

    if subscriber and not is_in_list:
        try:
            newsubscriber = Subscribers(subscriber["email"])
            db.session.add(newsubscriber)
            db.session.commit()

            return json.dumps({"message" : "Subscribed!", "status": "ok"})
        except:
            return json.dumps({"message" : "There was a problem adding you to the list. Try again later!", "status": "unsuccessful"})
    else:
        return json.dumps({"message" : "Your mail is allready in the list!", "status": "unsuccessful"})


@blog_app.route('/newsletter', methods=['GET', 'POST'])
@author_required
def newsletter():
    form = NewsletterForm()

    return render_template('blog/newsletter.html', form=form)
