from flask import Flask, request, render_template, redirect, url_for
import re
# from main import main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/eye', methods=['POST'])
def submit():
    # main()
    return redirect(url_for('index'))


@app.route('/signin ', methods=['POST', 'GET'])
def signin():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        if email == 'testing@example.com' and password == 'testing' :
            return redirect(url_for('index')) # render_template('index.html')
        else:
            msg = 'Invalid username'

    return render_template('signin.html', msg = msg)


        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        # account = cursor.fetchone()
        # if account:
        #    session['loggedin'] = True
        #    session['username'] = account['username']
        #    msg = 'Logged in successfully !'
        #    return render_template('index.html', msg = msg)
        #else:
        #    msg = 'Incorrect username / password !'
    #return render_template('signin.html', msg = msg)
    # return render_template('signin.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'username' in request.form:
        email = request.form['email'];
        username = request.form['username'];
        password = request.form['password'];

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers.'
        elif not username or not password or not email:
            msg = 'Please fill out the form'
        else:
            msg = 'Registration Successful'
            return redirect(url_for(index))

    return render_template('signup.html', msg = msg)



@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/python')    
def python():
    return render_template('python.html')


@app.route('/java')
def java():
    return render_template('java.html')

@app.route('/mysql')
def mysql():
    return render_template('mysql.html')

if __name__ == '__main__':
    app.run(debug=True)
