from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.completed_workout import CompletedWorkout
from flask_app.models.training import Training

@app.route("/complete_workout/<int:training_id>", methods=["GET", "POST"])
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
    print("Dashboard route called")
    if "user_id" not in session:
        print("No user in session, redirecting to home")
        return redirect('/')
    
    user_id = session["user_id"]
    data = {"user_id": user_id}

    print("Fetching all training")
    all_training = Training.get_all_training()
    print("Fetching completed workouts")
    completed_workouts = CompletedWorkout.get_completed_workouts_by_user(data)

    print("All Training: ", all_training) #Prints the all_training data
    print("Completed Workouts: ", completed_workouts) #Prints the completed_workouts data

    return render_template("dashboard.html", completed_workouts=completed_workouts, all_training=all_training)