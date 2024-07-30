import requests
import random




def get_random_workout():
    url = "https://wger.de/api/v2/exercise/?language=2"
    response = requests.get(url)
    exercises = response.json()['results']

    english_exercises = [exercise for exercise in exercises if exercise['description']]

    if not english_exercises:
        return {
            "workout": "No English workout available",
            "description": "Please try again later."
        }

    random_exercise = random.choice(english_exercises)

    description = random_exercise['description'].replace('<p>', '').replace('</p>', '').replace('\n', ' ')

    return{
        "workout": random_exercise['name'],
        "description": description
    }