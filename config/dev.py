import os

SECRET_KEY = "top-secret"
DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = 'test'
BLOG_DATABASE_NAME = 'blog'
DB_HOST = os.getenv('IP', '127.0.0.1')
DB_PORT = int(os.getenv('PORT', 3306))
DB_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format (DB_USERNAME, DB_PASSWORD,DB_HOST,DB_PORT, BLOG_DATABASE_NAME )
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOADED_IMAGES_DEST = 'C:/Users/serenity/Desktop/python_project/blog/blogapp/blogapp/static/img/'
UPLOADED_IMAGES_URL = '/static/img/'
