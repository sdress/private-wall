from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.message import Message

@app.route('/wall')
def show_wall():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    # print(data)
    return render_template('wall.html', user=User.get_from_id(data), all_users=User.get_all(), user_msgs=Message.get_user_msgs(data), sent_msgs=len(Message.get_sent_msgs(data)))

@app.route('/send-msg/<int:id>', methods = ['POST'])
def send_msg(id):
    if 'user_id' not in session:
        return redirect('/logout')
    print(request.form)
    data = {
        'content': request.form['content'],
        'sender_id': session['user_id'],
        'receiver_id': id,
    }
    print(data)
    Message.create(data)
    flash('Message sent!')
    return redirect('/wall')

@app.route('/delete-msg/<int:id>')
def delete_msg(id):
    data = {
        'id': id
    }
    Message.delete_msg(data)
    return redirect('/wall')