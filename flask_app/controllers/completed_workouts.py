from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.completed_workout import CompletedWorkout

@app.route("/complete_workout/<int:training_id>", methods=["POST"])
def complete_workout(training_id):
    if "user_id" not in session:
        return redirect('/')
    
    user_id = session["user_id"]
    data = {
        "user_id": user_id,
        "training_id": training_id
    }
    CompletedWorkout.complete_workout(data)

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect('/')
    
    user_id = session["user_id"]
    data = {"user_id": user_id}
    completed_workouts = CompletedWorkout.get_completed_workouts_by_user(data)

    return render_template("dashboard.html", completed_workouts=completed_workouts)