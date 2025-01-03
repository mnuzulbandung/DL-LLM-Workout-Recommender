from flask import Flask, jsonify, request, send_from_directory
import os
import json

# Initializes a Flask web application
app = Flask(__name__)

# Defines the folder (exercises) for storing exercise JSON files.
EXERCISES_FOLDER = 'exercises'


# Defines a Flask endpoint to list all exercise folders in the EXERCISES_FOLDER directory.
@app.route('/list_all', methods=['GET'])
def list_all_exercises():
    """Returns excercise list in the exercise folders directory as JSON"""
    try:
        folders = [folder_name for folder_name in os.listdir(EXERCISES_FOLDER)
                   if os.path.isdir(os.path.join(EXERCISES_FOLDER, folder_name))]
        return jsonify({"exercises": folders}), 200
    except Exception as e:
        return jsonify({"message": f"Error occurred: {str(e)}"}), 500


# Defines a Flask endpoint to get exercise-related images based on the provided exercise name and image number.
@app.route('/exercises/<exercise_name>/images/<image_number>.jpg', methods=['GET'])
def get_exercise_image(exercise_name, image_number):
    """Returns image 1 and 2 related to exercise_name var"""
    try:
        exercise_name = exercise_name.strip().lower()
        image_name = f"{image_number}.jpg"

        image_path = os.path.join(EXERCISES_FOLDER, exercise_name, image_name)

        if os.path.exists(image_path):
            return send_from_directory(os.path.join(EXERCISES_FOLDER, exercise_name), image_name)
        else:
            return jsonify({"message": "Image not found."}), 404
    except Exception as e:
        print(f"Error in get_exercise_image: {e}")
        return jsonify({"message": "Internal server error."}), 500


if __name__ == '__main__':
    app.run(debug=True)
