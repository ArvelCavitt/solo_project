from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, request, redirect, session, jsonify
from flask_app.models import user, training
from flask_app.models.user import User
from flask_app.models.friend_request import FriendRequest
from flask_app.models.completed_workout import CompletedWorkout
from flask_app.services.wger_service import get_random_workout


@app.route('/dashboard')
def home():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    print("session", session)

    print("Fetching all training")
    all_training = training.Training.get_all_training()
    print("Fetching completed workouts")
    completed_workouts = CompletedWorkout.get_completed_workouts_by_user(data)

    # for searching for friends i'm adding a get all users
    current_user_id = session['user_id']
    users = User.get_all_except_current(current_user_id)
    pending_friend_requests = FriendRequest.get_request_by_user_id(current_user_id)
    friends = FriendRequest.get_friends_by_user_id(current_user_id)

    return render_template("dashboard.html", user=user.User.get_id(data), all_training=all_training, completed_workouts=completed_workouts, pending_friend_requests=pending_friend_requests, friends=friends, users=users)

@app.route("/new")
def training_form():
    data = {
        'id': session['user_id']
    }
    return render_template("new_workout.html", user=user.User.get_id(data))

@app.route("/add_workout", methods=["POST"])
def add_workout():
    if "user_id" not in session:
        return redirect('/')
    if not training.Training.validate_training(request.form):
        return redirect("/new")
    data = {
        "workout": request.form.get("workout", ""),
        "breaks": request.form["breaks"],
        "date": request.form["date"],
        "description": request.form.get("description", ""),
        "youtube_url": request.form["youtube_url"],
        "user_id": session["user_id"]
    }
    training.Training.add_training(data)
    return redirect("/dashboard")

@app.route("/random_workout")
def random_workout():
    random_workout = get_random_workout()
    return jsonify(random_workout)

@app.route("/workouts/<int:id>")
def view_workouts(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id":id
    }
    workout = training.Training.get_one_training(data)
    return render_template("workouts.html", this_workout = workout)

@app.route("/edit/<int:id>")
def edit_workouts(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id":id
    }
    workout = training.Training.get_one_training(data)
    return render_template("edit_workouts.html", this_workout = workout)



@app.route("/delete/<int:id>")
def delete_training(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id":id
    }
    training.Training.delete_training(data)
    return redirect("/dashboard")


@app.route("/editing/<int:id>", methods=["POST"])
def editing_workout(id):
    if "user_id" not in session:
        return redirect('/')
    if not training.Training.validate_training(request.form):
        return redirect(f"/edit/{id}")  #  convert to f string later on
    data = {
        "workout": request.form["workout"],
        "breaks": request.form["breaks"],
        "date": request.form["date"],
        "description": request.form["description"],
        "youtube_url": request.form["youtube_url"],
        "id":id
    }
    training.Training.edit_training(data)
    return redirect("/dashboard")


@app.route('/friend/<int:friend_id>')
def view_friend(friend_id):
    query = "SELECT * FROM user WHERE id = %(id)s;"
    data = { 'id': friend_id }
    friend_info = connectToMySQL('fitness').query_db(query, data)

    workout_query = """
    SELECT training.*, completed_workouts.*
    FROM completed_workouts
    JOIN training ON training.id = completed_workouts.training_id
    WHERE training.user_id = %(user_id)s;
    """

    workout_data = {'user_id': friend_id}
    completed_workouts = connectToMySQL('fitness').query_db(workout_query, workout_data)

    if friend_info:
        return render_template('friend_profile.html', friend=friend_info[0], completed_workouts=completed_workouts)
    else:
        return "Friend not found", 404