from flask import Flask, render_template, request, url_for, redirect, session, g   

app = Flask(__name__)
app.secret_key = 'justinsakong'
class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

    def __repr__(self):
        return f'<User: {self.name}>'


users = []
users.append(User(id=1, name='justin', password='justin'))
users.append(User(id=2, name='sakong', password='sakong'))
print(users)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form.get('username')
        password = request.form.get('password')

        user = [x for x in users if x.name == username][0]

        if user and (user.password == password):
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))


    return render_template('login.html')

@app.route('/profile')
def profile():

    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)