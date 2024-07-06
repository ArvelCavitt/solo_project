from flask_app.config.mysqlconnection import connectToMySQL

class CompletedWorkout:
    db = "fitness"

    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.training_id = data['training_id']
        self.completed_at = data['completed_at']

    @classmethod
    def complete_workout(cls,data):
        query = "INSERT INTO completed_workouts (user_id, training_id, completed_at) VALUES (%(user_id)s, %(training_id)s, NOW())"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_completed_workouts_by_user(cls, data):
        query = """
            SELECT * FROM completed_workouts
            JOIN training ON completed_workouts.training_id = training.id
            WHERE completed_workouts.user_id = %(user_id)s;
        """
        results = connectToMySQL('your_db').query_db(query, data)
        completed_workouts = []
        for row in results:
            completed_workouts.append(cls(row))
        return completed_workouts