from flask import Flask, render_template, request, redirect, url_for, render_template_string

app = Flask(__name__)

USERNAME = "SaiyanSai"
PASSWORD = "P4$$W0RD"

@app.route('/')
def home():
    return render_template('home.html')

#This code is where the injection is intended to happen
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

#This code is intentionally vulnerable to XSS
@app.route('/greet', methods = ['GET'])
def greet():
    name = request.args.get('name')
    response = f"<h3>H3LL0, {name} !!!! </h3>"
    return render_template_string(response)
if __name__ == '__main__':
    app.run(debug=True)
    