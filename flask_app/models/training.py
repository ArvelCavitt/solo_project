from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Training:
    db = "fitness"

    def __init__(self,data):
        self.id = data["id"]
        self.workout = data["workout"]
        self.breaks = data["breaks"]
        self.date = data["date"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None

    @staticmethod
    def validate_training(training):
        is_valid = True
        print(training)
        if len(training["workout"]) < 3:
            flash("Workout must be at least 3 characters long.")
            is_valid = False
        if len(training["breaks"]) < 1:
            flash("You should take a moment and drink some water. Now you have 1 break.")
            is_valid = False
        if len(training["date"]) < 1:
            flash("If you don't indicate when to do it.. Then it won't get done!")
            is_valid = False
        if len(training["description"]) < 1:
            flash("Tell us how to complete this task.")
            is_valid = False
        return is_valid

    @classmethod
    def add_training(cls, data):
        query = "INSERT INTO training (workout, breaks, date, description, user_id) VALUES (%(workout)s, %(breaks)s, %(date)s, %(description)s, %(user_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all_training(cls):
        query = "SELECT * FROM training JOIN user ON training.user_id = user.id;"
        results = connectToMySQL(cls.db).query_db(query)
        print("results", results)
        if len(results) == 0:
            return[]
        else:
            trainings = []
            for row in results:
                training_obj = cls(row)
                user_dictionary = {
                    "id": row['user.id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['user.created_at'],
                    "updated_at": row['user.updated_at']
                }
                user_obj = user.User(user_dictionary)
                training_obj.user = user_obj
                trainings.append(training_obj)
            print("trainings",trainings)
            
            return trainings

    @classmethod
    def get_one_training(cls,data):
        query = "SELECT * FROM training JOIN user ON training.user_id = user.id WHERE training.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        if len(results) == 0:
            return None
        else:
            training_dictionary = results[0]
            training_obj = cls(training_dictionary)
            user_dictionary = {
                "id":training_dictionary['user.id'],
                "first_name":training_dictionary['first_name'],
                "last_name":training_dictionary['last_name'],
                "email":training_dictionary['email'],
                "password":training_dictionary['password'],
                "created_at":training_dictionary['user.created_at'],
                "updated_at":training_dictionary['user.updated_at']
            }
            user_obj = user.User(user_dictionary)
            training_obj.user = user_obj
            return training_obj

    @classmethod
    def delete_training(cls,data):
        query = "DELETE FROM training WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def edit_training(cls,data):
        query = "UPDATE training SET workout = %(workout)s, breaks = %(breaks)s, date = %(date)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)