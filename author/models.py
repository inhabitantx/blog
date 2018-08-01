from final_project import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    fullname = db.Column(db.String(80))
    email = db.Column(db.String(35), unique=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(60))
    is_author = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)

    post = db.relationship('Post', backref='author', lazy='dynamic')


    def __init__(self, fullname, email, username, password, is_author=False, is_admin=False, is_active=False):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.is_author = is_author
        self.is_admin = is_admin
        self.is_active = is_active

    def __repr__(self):
        return '<Author {}>'. format (self.username)
