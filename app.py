from flask import Flask, render_template, flash, redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from cs50 import SQL
import os
from functools import wraps


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite databse
db = SQL("sqlite:///data.db")

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check for user error
        checkUsername = db.execute("SELECT COUNT(*) FROM users WHERE username = ?", username)
        if not username:
            return apology("missing username")
        elif not password:
            return apology("missing password")
        elif checkUsername[0]["COUNT(*)"] == 1:
            return apology("username already exists")
        elif password != confirmation:
            return apology("password don't match")
        
        # Put new user inside database
        db.execute("INSERT INTO users (username, email, hash) VALUES(?, ?, ?)", username, email, generate_password_hash(password))

        # Log the user in after registering
        login = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = login[0]["id"]

        return redirect("/mywl")
    
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear() #Forget any userid

    if request.method == "POST":
        #Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        
        #Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        #Query database for username 
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)
        
        # Remenber which user has logged in
        session["user_id"] = rows[0]["id"]

        #Redirect user to homepage
        return redirect("/mywl")
    
    # User reached via GET
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/mywl", methods=["GET", "POST"])
@login_required
def mywl():
    if request.method == "POST":
        name = request.form.get("name")
        review = request.form.get("review")
        rating = int(request.form.get("stars")) + 1

        if not name:
            return redirect("/")

        db.execute("INSERT INTO watchlist (name, review, rating, userid) VALUES(?, ?, ?, ?)", name, review, rating, session["user_id"])

        return redirect("/mywl")
    
    # display the table if the user is in GET method
    else:
        rows = db.execute("SELECT * FROM watchlist where userid = ?", session["user_id"])

        return render_template("mywl.html", database=rows)

@app.route("/friendswl", methods=["GET","POST"])
@login_required
def friendswl():
    if request.method == "POST":
        username = request.form.get("username")

        if not username:
            return redirect("/friendswl")
        
        rows = db.execute("SELECT * FROM watchlist JOIN users ON watchlist.userid = users.id WHERE users.username = ?", username)

        return render_template("friendswl.html", watchlist=rows, friend_username = username)

    else:
        return render_template("friendswl.html")


    

if __name__ == '__main__':
    app.run(debug=True)