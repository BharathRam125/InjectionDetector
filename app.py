from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

USERNAME = "SaiyanSai"
PASSWORD = "P4$$W0RD"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST' : 
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('home'))
        else:
            return 'Invalid Username or Password'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)