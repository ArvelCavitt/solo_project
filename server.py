from flask_app import app
from flask_app.controllers import users, trainings, completed_workouts, friend_requests


if __name__=="__main__":
    app.run(debug=True)