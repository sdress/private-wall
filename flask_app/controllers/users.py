from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def show_home_page():
    return render_template('login_reg.html')

@app.route('/create-user', methods=['POST'])
def create_user():
    if not User.validate(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect('/wall')

@app.route('/login', methods=['POST'])
def login_user():
    data = {
        'email': request.form['email']
    }
    user = User.get_from_email(data)
    if not user:
        flash('Email not found')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Incorrect password!')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/wall')

@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')

# '/wall' moved to messages.py

# @app.route('/wall')
# def show_wall():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         'id': session['user_id']
#     }
#     print(data)
#     return render_template('wall.html', user=User.get_from_id(data), all_users=User.get_all())