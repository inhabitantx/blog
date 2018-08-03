
from flask import redirect, request, url_for, session, jsonify
import json
from datetime import datetime

from blog.models import Comment,Reply, Post


from flask import Blueprint

comment_app = Blueprint('comment_app', __name__)




@comment_app.route("/comment/<int:post_id>" , methods=['GET', 'POST'])
def comment(post_id):

    article = Post.query.get(post_id)
    comments = article.comment.filter_by(is_live=True).all()

    if request.form.get('name') and request.form.get('email') and request.form.get('body'):
        article.add_comment(post_id, request.form.get('name'), request.form.get('email'), request.form.get('body'))
        #reply = Reply()

    return redirect(url_for('blog_app.article', slug=article.slug, comments=comments))

@comment_app.route("/newreply", methods=['GET', 'POST'])
def newreply():

    comment_id = request.form.get('comment_id')
    parent_id = 0
    if request.form.get('parent_id'):
        parent_id = request.form.get('parent_id')

    comment = Comment.query.get(comment_id)
    post_id = comment.post_id

    print(post_id)

    if(parent_id):
        reply = Reply.query.get(parent_id)

        if request.form.get('name') and request.form.get('email') and request.form.get('body'):
            try:
                reply.addchildren(comment.post_id, comment_id, parent_id, request.form.get('name'), request.form.get('email'), request.form.get('body'))
            except:
                print("addchildren")
    else:
        if request.form.get('name') and request.form.get('email') and request.form.get('body'):
            try:
                comment.add_reply(post_id,comment_id, request.form.get('name'), request.form.get('email'), request.form.get('body'))
            except:
                print("add_reply")

    return json.dumps({"message" : "Reply added successfully"})



@comment_app.route('/getreplies', methods=['GET', 'POST'])
def getreplies():

    content = request.get_json(force=True)
    comment = Comment.query.get(content["comment_id"])
    replies = comment.replies.filter_by(is_live=True).all()

    if replies:
        allrows = []
        for reply in replies:
            allrows.append({"name" : reply.name, "date" : reply.publish_date.strftime('%d-%m-%y'), "body": reply.body, "parent_id" : reply.parent_id,"id" : reply.id, "comment_id" : reply.comment_id})

        return json.dumps(allrows)
    else:
        return json.dumps({'error': 'Could not fetch replies!'})
