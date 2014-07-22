import urlparse

from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    url = db.Column(db.String)
    score = db.Column(db.Integer)

    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.score = 1

    @property
    def hostname(self):
        return urlparse.urlparse(self.url).hostname

db.create_all()

@app.route('/')
def index():
    return render_template('index.html', posts=Post.query.order_by(-Post.score)[:25])

@app.route('/posts/', methods=('POST',))
def new_post():
    post = Post(request.form['title'], request.form['url'])
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/posts/<int:post_id>/upvote', methods=('POST',))
def upvote(post_id):
    post = Post.query.filter_by(id=post_id).one()
    post.score = Post.score + 1
    db.session.commit()
    return str(post.score)

@app.route('/posts/<int:post_id>/downvote', methods=('POST',))
def downvote(post_id):
    post = Post.query.filter_by(id=post_id).one()
    post.score = Post.score - 1
    db.session.commit()
    return str(post.score)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
