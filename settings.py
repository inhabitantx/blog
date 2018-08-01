import os

SECRET_KEY = "sadjfläsajdfäpoiasüporwäpeojrq+w0ß9e8r23854üiäpläsA´fasd8f´ß09sidöäaljräq2j35rü098dß0f9uwqlkneräljadsü9f"
DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = 'test'
BLOG_DATABASE_NAME = 'blog'
DB_HOST = os.getenv('IP', '127.0.0.1')
DB_PORT = int(os.getenv('PORT', 3306))
DB_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format (DB_USERNAME, DB_PASSWORD,DB_HOST,DB_PORT, BLOG_DATABASE_NAME )
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOADED_IMAGES_DEST = 'C:/Users/serenity/Desktop/python_project/studies/final_project/static/img/'
UPLOADED_IMAGES_URL = '/static/img/'
