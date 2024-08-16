from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class FriendRequest:
    db = "fitness"

    def __init__(self, data):
        self.id = data['id']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.status = data['status']
        self.created_at = data['created_at']
        self.sender_first_name = data.get('sender_first_name')
        self.sender_last_name = data.get('sender_last_name')

    @classmethod
    def send_request(cls, data):
        # This will check if a request already exists or if they are already friends
        query = """
        SELECT * FROM friend_requests 
        WHERE (sender_id = %(sender_id)s AND receiver_id = %(receiver_id)s)
        OR (sender_id = %(receiver_id)s AND receiver_id = %(sender_id)s);
        """
        existing_requests = connectToMySQL(cls.db).query_db(query, data)

        if len(existing_requests) > 0:
            flash('Friend request already sent or you are already friends!')
            return False

        # If there are no existing request we can insert a new friend request

        query = """
        INSERT INTO friend_requests (sender_id, receiver_id, status, created_at)
        VALUES (%(sender_id)s, %(receiver_id)s, %(status)s, NOW());
        """
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_request_by_user_id(cls, user_id):
        # query = "SELECT * FROM friend_requests WHERE receiver_id = %(user_id)s AND status = 'pending';"
        # results = connectToMySQL(cls.db).query_db(query, {'user_id': user_id})

        query = """
        SELECT fr.*, u.first_name as sender_first_name, u.last_name as sender_last_name
        FROM friend_requests fr
        JOIN user u ON fr.sender_id = u.id
        WHERE fr.receiver_id = %(user_id)s AND fr.status = 'pending';
        """
        results = connectToMySQL(cls.db).query_db(query, {'user_id': user_id})
        friend_requests = []
        for row in results:
            friend_requests.append(cls(row))
        return friend_requests
    
    @classmethod
    def update_request_status(cls, data):
        query = """
        UPDATE friend_requests
        SET status = %(status)s
        WHERE id = %(id)s
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_friends_by_user_id(cls, user_id):
        query = """
        SELECT u.*
        FROM friend_requests fr
        JOIN user u ON (fr.sender_id = u.id  OR fr.receiver_id = u.id)
        WHERE (fr.sender_id = %(user_id)s OR fr.receiver_id = %(user_id)s)
        AND fr.status = 'accepted' AND u.id != %(user_id)s;
        """

        results = connectToMySQL(cls.db).query_db(query, {'user_id': user_id})
        friends = []
        for row in results:
            friends.append(user.User(row))
        return friends