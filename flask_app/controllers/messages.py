from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User

@app.route('/wall')
def show_wall():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    # print(data)
    return render_template('wall.html', user=User.get_from_id(data), all_users=User.get_all())

@app.route('/send-msg/<int:id>')
def send_msg(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id,
        'content': request.form['content'],
        
    }

