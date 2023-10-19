from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, training


@app.route('/dashboard')
def home():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    print("session", session)
    return render_template("dashboard.html", user=user.User.get_id(data), all_training = training.Training.get_all_training())

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
        "workout": request.form["workout"],
        "breaks": request.form["breaks"],
        "date": request.form["date"],
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    training.Training.add_training(data)
    return redirect("/dashboard")

@app.route("/workouts/<int:id>")
def view_workouts(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id":id
    }
    return render_template("workouts.html", this_workout = training.Training.get_one_training(data))

@app.route("/edit/<int:id>")
def edit_workouts(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id":id
    }
    return render_template("edit_workouts.html", this_workout = training.Training.get_one_training(data))

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
        "id":id
    }
    training.Training.edit_training(data)
    return redirect("/dashboard")