import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/get_comments")
def get_comments():
    comments = mongo.db.comments.find()
    return render_template("comments.html", comments=comments)


@app.route("/")
@app.route("/get_ratings")
def get_ratings():
    ratings = mongo.db.ratings.find()
    return render_template("ratings.html", ratings=ratings)


@app.route("/")
@app.route("/get_trails")
def get_trails():
    trails = mongo.db.trails.find()
    return render_template("trails.html", trails=trails)


@app.route("/")
@app.route("/get_users")
def get_users():
    users = mongo.db.users.find()
    return render_template("users.html", users=users)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
