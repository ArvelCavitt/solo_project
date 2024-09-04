from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def reg():
    return render_template('register.html')

@app.route('/login')
def log():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "age": request.form['age'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "location": request.form['location']
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route("/my_training")
def my_training():
    return render_template("my_training.html")

@app.route('/edit_about_me', methods=['GET', 'POST'])
def edit_about_me():
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session['user_id']

    if request.method == 'POST':
        about_me = request.form['about_me']
        data = {
            'id': user_id,
            'about_me': about_me
        }
        User.update_about_me(data)
        return redirect('/dashboard')
    
    user = User.get_by_id({'id': user_id})
    return render_template('edit_about_me.html', user=user)