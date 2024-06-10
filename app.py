from flask import Flask, request, render_template, redirect, url_for, session
import re
import mysql.connector
#from main import main

app = Flask(__name__)

app.secret_key = "1112222333" # random key


connection = mysql.connector.connect(
    host="localhost", user="root", password="", database="pyworld"
)

@app.route("/")
def index():
    if 'email' in session:
        logged_in = True
    else:
        logged_in = False

    return render_template("index.html", logged_in=logged_in)


@app.route("/eye", methods=["POST"])
def submit():
#    main()
    return redirect(url_for("index"))


@app.route('/voice', methods=["POST"])
def voice():
    page = request.json['text']

    if page == 'home':
        return redirect(url_for('index'))
    elif page == 'get started':
        return redirect(url_for('signin'))
    elif page == 'java':
        return redirect(url_for('java'))
    elif page == 'python':
        return redirect(url_for('python'))
    elif page == 'mysql':
        return redirect(url_for('mysql'))
    elif page == 'contact':
            return redirect(url_for('contact'))
    elif page == 'logout':
            return redirect(url_for('logout'))
    elif page == 'about':
        return redirect(url_for('about'))
    else:
        return "Command not recognized"


@app.route("/signin ", methods=["POST", "GET"])
def signin():
    if 'email' in session:
        logged_in = True
    else:
        logged_in = False

    msg = ""
    if (
        request.method == "POST"
        and "email" in request.form
        and "password" in request.form
    ):
        email = request.form["email"]
        password = request.form["password"]

        cursor = connection.cursor()
        cursor.execute("Select * from users where useremail = %s and password = %s", (email, password, ))
        account = cursor.fetchone()

        if account:
            session['email'] = email
            return redirect("/")  # render_template('index.html')
        else:
            msg = "Invalid username or password"

    return render_template("signin.html", msg=msg, logged_in=logged_in)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if 'email' in session:
        logged_in = True
    else:
        logged_in = False

    msg = ""
    if (
        request.method == "POST"
        and "email" in request.form
        and "password" in request.form
        and "username" in request.form
    ):
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        account = cursor.fetchone()

        if account:
            msg = "user already exist"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Invalid email address"
        elif not re.match(r"[A-Za-z0-9]+", username):
            msg = "Username must contain only characters and numbers."
        elif not username or not password or not email:
            msg = "Please fill out the form"
        else:
            cursor.execute(
                "Insert into users values (null, %s, %s, %s)",
                (username, email, password),
            )
            connection.commit()
            msg = "Registration Successful"
            session['email'] = email
            return redirect("/")

    return render_template("signup.html", msg=msg, logged_in=logged_in)


@app.route("/contact")
def contact():
    if 'email' in session:
        logged_in = True
    else:
        logged_in = False

    return render_template("contact.html", logged_in=logged_in)


@app.route("/about")
def about():
    if 'email' in session:
        logged_in = True
    else:
        logged_in = False

    return render_template("about.html", logged_in=logged_in)


@app.route("/python")
def python():
    if 'email' in session:
        logged_in = True
    else:
        logged_in = False

    return render_template("python.html", logged_in=logged_in)


@app.route("/java")
def java():
    if 'email' in session:
        logged_in = True
    else:
        logged_in = False

    return render_template("java.html", logged_in=logged_in)


@app.route("/mysql")
def mysql():
    if 'email' in session:
        logged_in = True
    else:
        logged_in = False

    return render_template("mysql.html", logged_in=logged_in)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
