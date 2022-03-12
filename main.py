import datetime

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField


## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Bootstrap(app)
# ckeditor=CKEditor(app)
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

class CreatePostForm(FlaskForm):
    title = StringField(label="Title", validators=[DataRequired()])
    subtitle = StringField(label="Subtitle", validators=[DataRequired()])
    author = StringField(label="Author Name", validators=[DataRequired()])
    img_url = StringField(label="Img_url", validators=[URL()])
    body = CKEditorField(label="Story", validators=[DataRequired()])
    submit = SubmitField("Submit")





@app.route("/")
def home():
    posts = BlogPost().query.all()
    return render_template("index.html", all_posts=posts)

@app.route("/post")
def show_post():
    index = request.args.get("index")
    requested_post = BlogPost().query.get(index)
    return render_template("post.html", post=requested_post)

@app.route("/edit_post", methods=["GET", "POST"])
def edit_post():
    post_name = "Edit Post"
    index = request.args.get("post_id")
    requested_post = BlogPost().query.get(index)
    newform = CreatePostForm(title=requested_post.title,
                             subtitle=requested_post.subtitle,
                             author=requested_post.author,
                             img_url=requested_post.img_url,
                             body=requested_post.body)
    if newform.validate_on_submit():
        requested_post.title = newform.title.data
        requested_post.subtitle = newform.subtitle.data
        requested_post.date = datetime.date.today().strftime("%B %d %Y")
        requested_post.author = newform.author.data
        requested_post.body = newform.body.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", form=newform, post_name=post_name)


@app.route("/new_post", methods=["GET", "POST"])
def new_post():
    post_name="New Post"
    form= CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(title=form.title.data,
                            subtitle=form.subtitle.data,
                            date=datetime.date.today().strftime("%B %d %Y"),
                            body=form.body.data,
                            author=form.author.data)
        db.session.add(new_post)
        db.session.commit()
        redirect(url_for("home"))
    return render_template("make-post.html",form=form, post_name=post_name)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# @app.route("/delete")
# def delete():
#     del_id = request.args.get(id)
#     to_delete = BlogPost().query.get(del_id)
#     db.session.delete(to_delete)
#     return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(
        port=5000,debug=True)


