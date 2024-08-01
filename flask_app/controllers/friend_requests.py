from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.friend_request import FriendRequest
from flask_app.models.user import User

@app.route('/send_friend_request', methods=['POST'])
def send_friend_request():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'sender_id': session['user_id'],
        'receiver_id': request.form['receiver_id'],
        'status': 'pending'
    }

    FriendRequest.send_request(data)
    flash('Friend request sent!')
    return redirect('/dashboard')

@app.route('/friend_requests')
def friend_requests():
    if 'user_id' not in session:
        return redirect('/')
    
    friend_requests = FriendRequest.get_request_by_user_id(session['user_id'])
    return render_template('friend_requests.html', friend_requests=friend_requests)

@app.route('/update_friend_request/<int:id>', methods=['POST'])
def update_friend_request(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id': id,
        'status': request.form['status']
    }
    
    FriendRequest.update_request_status(data)
    return redirect('/friend_requests')