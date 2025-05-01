from flask import Flask, render_template, request, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = 'vulnerable_secret'

users = {
    "admin": {
        "password": "password123",
        "role": "admin",
        "email": "admin@example.com"
    },
    "user": {
        "password": "userpass",
        "role": "user",
        "email": "user@example.com"
    }
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        return "Invalid credentials"
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/csrf', methods=['GET', 'POST'])
def csrf():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_pass = request.form.get('new_password')
        users[session['username']]['password'] = new_pass
        return "Password changed!"
    return render_template('csrf.html')


@app.route('/xss')
def xss():
    q = request.args.get('q', '')
    return render_template('xss.html', q=q)


@app.route('/idor')
def idor():
    user = request.args.get('user')
    info = users.get(user)
    if info:
        return render_template('idor.html', user=user, email=info['email'])
    return "User not found"


@app.route('/admin')
def admin():
    if session.get('username'):
        return render_template('admin.html', user=session['username'])
    return abort(403)


if __name__ == '__main__':    
    app.run()
