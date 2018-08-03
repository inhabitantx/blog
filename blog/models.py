from blogapp.app import db
from blogapp.app import uploaded_images
from datetime import datetime

from blogapp.comment.models import Comment,Reply


keyword_intermed = db.Table(
    'keyword_intermed',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keywords.id')),
)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    admin = db.Column(db.Integer, db.ForeignKey('author.id'))
    posts = db.relationship('Post', backref='blog', lazy='dynamic')


    def __init__(self, name, admin):
        self.name = name
        self.admin = admin


    def __repr__(self):
        return '<Blog {} >'.format(self.name)



class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img = db.Column(db.String(256))
    slug = db.Column(db.String(256), unique=True)
    publish_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)
    maincategory_id = db.Column(db.Integer, db.ForeignKey('main_category.id'))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('sub_category.id'))
    subsubcategory_id = db.Column(db.Integer, db.ForeignKey('sub_sub_category.id'))

    keywords = db.relationship('Keywords', secondary=keyword_intermed, back_populates="posts")
    maincategory = db.relationship('MainCategory', backref=db.backref('posts', lazy='dynamic'))
    subcategory = db.relationship('SubCategory', backref=db.backref('posts', lazy='dynamic'))
    subsubcategory = db.relationship('SubSubCategory', backref=db.backref('posts', lazy='dynamic'))

    comment = db.relationship('Comment', backref='post', lazy='dynamic')
    reply = db.relationship('Reply', backref='post', lazy='dynamic')

    def add_keywords(self,keywordarray):
        for keyword in keywordarray:
            if(Keywords.query.filter_by(keyword=keyword).first()):
                newkeyword = Keywords.query.filter_by(keyword=keyword).first()
            else:
                newkeyword = Keywords(keyword)

            self.keywords.append(newkeyword)

            db.session.add(self)
            db.session.commit()

    @property
    def imgsrc(self):
        return uploaded_images.url(self.img)

    def add_comment(self, post_id, name, email, body):
        comment = Comment(post_id, name, email, body)

        db.session.add(comment)
        db.session.commit()



    def __init__(self, blog, author, title, body, maincategoryid, subcategoryid, subsubcategoryid, image = None, slug=None, publish_date=None, live=True):
        self.blog_id = blog.id
        self.author_id = author.id
        self.title = title
        self.body = body
        self.maincategory_id = maincategoryid
        self.subcategory_id = subcategoryid
        self.subsubcategory_id = subsubcategoryid
        self.img = image
        self.slug = slug
        if publish_date == None:
            self.publish_date = datetime.utcnow()
        else:
            self.publish_date = publish_date
        self.live = live

    def __repr__(self):
        return "<Post {}>".format(self.title)



class Keywords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(60), unique=True)

    posts = db.relationship('Post', secondary=keyword_intermed, back_populates='keywords')

    def __init__(self, keyword):
        self.keyword = keyword

    def __repr__(self):
        return self.keyword

class MainCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))

    subcategories = db.relationship('SubCategory' , backref='maincategory', lazy='dynamic')


    def add_subcategory(self,name, maincategoryid):
        subcategory = SubCategory(name, maincategoryid)

        db.session.add(subcategory)
        db.session.commit()


    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return self.name



class SubCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    main_category_id = db.Column(db.Integer, db.ForeignKey('main_category.id'))

    subsubcategories = db.relationship('SubSubCategory' , backref='subcategory', lazy='dynamic')


    def add_subsubcategory(self, name, subcategoryid):
        subsubcategory = SubSubCategory(name, subcategoryid)

        db.session.add(subsubcategory)
        db.session.commit()

    def __init__(self, name, maincategoryid):
        self.name = name
        self.main_category_id = maincategoryid

    def __repr__(self):
        return self.name

class SubSubCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    sub_category_id = db.Column(db.Integer, db.ForeignKey('sub_category.id'))

    def __init__(self, name, subcategoryid):
        self.name = name
        self.sub_category_id = subcategoryid

    def __repr__(self):
        return self.name

class Subscribers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60))
    subscription_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean)


    def __init__(self, email, is_active=True):
        self.email = email
        self.subscription_date = datetime.utcnow()
        self.is_active = is_active

    def __repr__(self):
        return f"<{self.email}>"
