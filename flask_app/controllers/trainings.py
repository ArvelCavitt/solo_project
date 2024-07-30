from flask_app import app
from flask import render_template, request, redirect, session, jsonify
from flask_app.models import user, training
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

    return render_template("dashboard.html", user=user.User.get_id(data), all_training=all_training, completed_workouts=completed_workouts)

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