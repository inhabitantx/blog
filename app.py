import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES

db = SQLAlchemy()

uploaded_images = UploadSet('images', IMAGES)

def create_app(config_type):
    app = Flask(__name__)

    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')
    app.config.from_pyfile(configuration)

    configure_uploads(app, uploaded_images)
    from blogapp.blog.views import blog_app
    from blogapp.author.views import author_app
    from blogapp.admin.views import admin_app
    from blogapp.comment.views import comment_app

    app.register_blueprint(blog_app)
    app.register_blueprint(author_app)
    app.register_blueprint(admin_app)
    app.register_blueprint(comment_app)

    db.init_app(app)

    return app
