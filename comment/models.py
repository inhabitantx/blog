from blogapp.app import db
from datetime import datetime



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    name = db.Column(db.String(80))
    email = db.Column(db.String(60), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_live = db.Column(db.Boolean)
    publish_date = db.Column(db.DateTime)

    replies = db.relationship('Reply', backref='comment', lazy='dynamic')

    def add_reply(self,post_id, comment_id, name, email, body , parent_id = 0):
        reply = Reply(post_id,comment_id, name, email, body, parent_id)

        db.session.add(reply)
        db.session.commit()

    def approve_comment(comment_id, is_live=True):
        comment = Comment.query.get(comment_id)
        comment.is_live = is_live

        db.session.add(comment)
        db.session.commit()

    def delete_comment(comment_id):
        comment = Comment.query.get(comment_id)

        db.session.delete(comment)
        db.session.commit()


    def __init__(self, post_id, name, email, body, is_live=False, publish_date=None):
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body
        self.is_live = is_live
        if publish_date == None:
            self.publish_date = datetime.utcnow()
        else:
            self.publish_date = publish_date

    def __repr__(self):
        return f"<{self.email}, {self.publish_date}"

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_id = db.Column(db.Integer,db.ForeignKey('comment.id'))
    parent_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    email = db.Column(db.String(60), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_live = db.Column(db.Boolean)
    publish_date = db.Column(db.DateTime)

    children = db.relationship('Reply', primaryjoin = parent_id == id,foreign_keys = id, remote_side=parent_id)

    def addchildren(self, post_id, comment_id, parent_id, name, email, body):
        children = Reply(post_id, comment_id, name, email, body, parent_id)

        db.session.add(children)
        db.session.commit()

    def approve_reply(reply_id, is_live=True):
        reply = Reply.query.get(reply_id)
        reply.is_live = is_live

        db.session.add(reply)
        db.session.commit()

    def delete_reply(reply_id):
        reply = Reply.query.get(reply_id)

        db.session.delete(reply)
        db.session.commit()


    def __init__(self,post_id,comment_id,name,email,body,parent_id = 0,is_live=False,publish_date=None):
        self.post_id = post_id
        self.comment_id = comment_id
        self.parent_id = parent_id
        self.name = name
        self.email = email
        self.body = body
        self.is_live = is_live
        if publish_date == None:
            self.publish_date = datetime.utcnow()
        else:
            self.publish_date = publish_date

    def __repr__(self):
            return f"<{self.name}, {self.email}>"
