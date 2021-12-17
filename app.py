from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    posted_author = db.Column(db.String(30),nullable=False,default='zambbo')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(40),nullable=False)
    posts = db.relationship('Post',backref='category')


db.create_all()
db.session.commit()

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/posts/category",methods=['GET'])
def category():
    if request.method == 'GET':
        categorys = Category.query.order_by(Category.category_name).all()
        return render_template('category.html',categorys=categorys)
    else:
        return redirect('index') 

@app.route("/new",methods=['GET','POST'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        post = request.form['post']
        category = request.form['category']

        #If category was not exsits, add category to db 

        if Category.query.filter_by(category_name=category).first() == None:
            new_category = Category(category_name = category)
            db.session.add(new_category)
            db.session.commit()
        
        category_record = Category.query.filter_by(category_name=category).first()
        new_post = Post(title=title, content=post,category_id = category_record.id)
        db.session.add(new_post)
        db.session.commit()

        
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('new_post.html')        

@app.route('/posts/category/<string:category>', methods=['GET'])
def post(category):
    if request.method == 'GET':
        category_posts = Category.query.filter_by(category_name=category).first().posts
        return render_template('category_posts.html',posts=category_posts)
    else:
        pass
