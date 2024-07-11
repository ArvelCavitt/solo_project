from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, training

class CompletedWorkout:
    db = "fitness"

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.training_id = data['training_id']
        self.completed_at = data['completed_at']
        self.workout = data.get('workout')
        self.description = data.get('description')
        self.breaks = data.get('breaks')

    @classmethod
    def complete_workout(cls, data):
        query = "INSERT INTO completed_workouts (user_id, training_id, completed_at) VALUES (%(user_id)s, %(training_id)s, NOW())"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_completed_workouts_by_user(cls, data):
        query = """
        SELECT * training.workout, training.description, training.breaks 
        FROM completed_workouts
        JOIN training ON completed_workouts.training_id = training.id
        WHERE completed_workouts.user_id = %(user_id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        print("Completed Workouts Query Results: ", results)  # Print the raw query results
        completed_workouts = []
        if results:
            for row in results:
                completed_workouts.append(cls(row))
                print("Completed Workout Row Processed: ", row)  # Print each row processed
        else:
            print("No completed workouts found for user_id: ", data['user_id'])
        return completed_workouts