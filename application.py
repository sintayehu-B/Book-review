
from forms import *
# from imports import *
import requests
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask import Flask, session
# from flask_session import Session
from sqlalchemy import create_engine, text
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_login import login_user, UserMixin ,current_user
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy
# from sqlite3


app = Flask(__name__)
app.config["SECRET_KEY"] = "051277379b285b544ff835e235bf0e658e22d1"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://slniyhprhdecdt:4c47420a0456d96c614a9136f5aa850f90a5f76370da0abe0d294ad755eace47@ec2-18-215-111-67.compute-1.amazonaws.com:5432/d2k26gq36rcfe0"
# db = SQLAlchemy(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


engine = SQLAlchemy(app).engine
bcrypt = Bcrypt(app)


@app.route("/")
@app.route("/home")
def index():
    if "logged_in" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", title="Home")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if "logged_in" in session:
#         return redirect(url_for("index"))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         try:
#             hashed_password = bcrypt.generate_password_hash(
#                 form.password.data).decode("utf-8")
#             user = f""" INSERT INTO Users (User_Name, Email, password), values ('{form.username.data}','{form.email.data}','{hashed_password}') """
#             engine.execute(user)
#             session["logged_in"] = True
#             session["email"] = form.email.data
#             session["username"] = form.username.data
#             flash(
#                 f"Your Account has been created! your are now able to log in {form.username.data}!", "success")
#         except:
#             flash("User already exists.", "danger")
#             return render_template("register.html", form=form)
#         return redirect(url_for("login"))

#     return render_template("register.html", title="Register", form=form)


@app.route("/login",  methods=["GET", "POST"])
def login():
    if "logged_in" in session:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = engine.execute(text(
            f""" SELECT * FROM Users WHERE User_Name= '{form.username.data}' """)).fetchone()

        if user and bcrypt.check_password_hash(user["password"], form.password.data):

            session["logged_in"] = True
            session["username"] = form.username.data
            return redirect(url_for("index"))
        else:
            flash("login unsuccessful", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/search", methods=["GET", "POST"])
def search():

    if request.method == "POST":

        if session.get("{username.data}"):
            return render_template('search.html', logout=True)

        book_query = request.form.get("search")
        book_query_like = '%' + book_query + '%'

        books = engine.execute(text("""SELECT * FROM Books WHERE Isbn LIKE :book_query_like OR Title LIKE :book_query_like OR Author LIKE :book_query_like"""),
                               {"book_query_like": book_query_like}).fetchall()

        # get search input

        # list books for user

        return render_template("search.html", no_books=(len(books) == 0), books=books)

    # make sure that user is logging in
    if not session.get("logged_in"):
        return render_template("search.html", logout=True)
    return render_template("search.html", logout=False)


@app.route("/book_detail", methods=["GET", "POST"])
def book_detail():
    print(session)
    if session.get("logged_in") is not None:
        isbn = request.args.get("isbn")
        # print(isbn)
        if not isbn:
            return ("404", 404)
        # username = session.get['username']
        book = engine.execute(
            f"""SELECT * FROM Books WHERE Isbn= '{isbn}' """,).fetchone()
        # Api
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": "Cdjuz7jTYIwy5Jj9GhY9sw", "isbns": isbn})
        average_rating = res.json()['books'][0]['average_rating']
        work_ratings_count = res.json()['books'][0]['work_ratings_count']
        print(request.method)
        if request.method == "POST":
            username = session["username"]
            review = request.form.get("comments")
            rating = request.form.get("rating")
            userratingQuery = text(
                f"SELECT * FROM Reviews WHERE User_Id = '{username}'")
            uresult = engine.execute(userratingQuery).fetchone()
            if not uresult:
                engine.execute(
                    f"""INSERT INTO Reviews (User_Id, Book_Isbn, rating, review) VALUES ('{username}', '{isbn}', '{rating}', '{review}')""")
            else:
                flash("You have already reviewed this book")
                print("++++++++++++++=MULTIPLE REVIEWS ARE NOT ALLOWED+++++++++++")

            ratingQuery = text(
                f"SELECT * FROM Reviews WHERE Book_Isbn = '{isbn}'")
            result = engine.execute(ratingQuery).fetchall()
            print(result)
            return render_template("book_detail.html", book=book, average_rating=average_rating, work_ratings_count=work_ratings_count, Reviews=result)
        else:
            ratingQuery = text(
                f"SELECT * FROM Reviews WHERE Book_Isbn = '{isbn}'")
            result = engine.execute(ratingQuery).fetchall()
            return render_template("book_detail.html", book=book, average_rating=average_rating, work_ratings_count=work_ratings_count, Reviews=result)
    return redirect(url_for('login'))


@app.route("/api/<isbn>")
def api_url(isbn):
    res = db.execute("select * from books where isbn=:isbn;",
                     {'isbn': isbn}).fetchone()
    if res == None:
        return jsonify({
            "error": "Invalid isbn.",
            "message": "Please insert a valid isbn."
        }), 404
    try:
        count, rating = get_review_statistics(res.id)
    except:
        count, rating = 0, 0

    return jsonify({
        "title": res.title,
        "author": res.author,
        "year": res.year,
        "isbn": res.isbn,
        "review_count": count,
        "average_score": rating
    }), 200


@ app.route("/logout")
def logout():
    session.clear()
    flash("Logout successful.", "successful")
    return redirect(url_for("login"))


if __name__ == "__main__":
    # app.debug = True
    app.run()
