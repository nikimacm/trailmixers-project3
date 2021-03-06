import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_index")
def get_index():
    index = mongo.db.index.find()
    return render_template("index.html", index=index)


@app.route("/index")
def index():
    return render_template("index.html", index=index)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    trails = list(mongo.db.trails.find({"$text": {"$search": query}}))
    return render_template("trails.html", trails=trails)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check for existing user in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "email": request.form.get("email").lower(),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_trail", methods=["GET", "POST"])
def add_trail():
    if request.method == "POST":
        trails = {
            "trail_title": request.form.get("trail_title"),
            "trail_address": request.form.get("trail_address"),
            "trail_created_by": session["user"],
            "trail_description": request.form.get("trail_description"),
            "trail_difficulty": request.form.get("trail_difficulty"),
            "trail_directions": request.form.get("trail_directions")
        }
        mongo.db.trails.insert_one(trails)
        flash("Trail Successfully Added")
        return redirect(url_for("trails"))

    trails = mongo.db.trails.find().sort("trails_difficulty", 1)
    return render_template("add_trail.html", trails=trails)


@app.route("/trails")
def trails():
    trails = list(mongo.db.trails.find())
    return render_template("trails.html", trails=trails)


@app.route("/edit_trail/<trail_id>", methods=["GET", "POST"])
def edit_trail(trail_id):
    if request.method == "POST":
        submit = {
            "trail_title": request.form.get("trail_title"),
            "trail_address": request.form.get("trail_address"),
            "trail_created_by": session["user"],
            "trail_description": request.form.get("trail_description"),
            "trail_difficulty": request.form.get("trail_difficulty"),
            "trail_directions": request.form.get("trail_directions")
        }
        mongo.db.trails.update({"_id": ObjectId(trail_id)}, submit)
        flash("Trail Successfully Updated")

    trail = mongo.db.trails.find_one({"_id": ObjectId(trail_id)})
    trails = mongo.db.trails.find().sort("trail_title", 1)
    return render_template("edit_trail.html", trail=trail, trails=trails)


@app.route("/delete_trail/<trail_id>")
def delete_trail(trail_id):
    mongo.db.trails.remove({"_id": ObjectId(trail_id)})
    flash("Trail Successfully Deleted")
    return redirect(url_for("get_index"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "0.0.0.0"),
            port=int(os.environ.get("PORT", "5000")),
            debug=True)
