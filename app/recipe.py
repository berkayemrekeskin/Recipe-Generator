from flask import Blueprint, render_template, request, session
from app.db import create_connection
import ollama 
import json

recipe_bp = Blueprint('recipe_bp', __name__)
@recipe_bp.route('/', methods=['GET', 'POST'])    
def index():
    return render_template('index.html')
    
@recipe_bp.route('/recipe', methods=['GET', 'POST'])
def recipe():
    if request.method == 'POST':
        
        ingredients = request.form.get('ingredients')
        model = "llama3.2"
        prompt = """
            The user will provide a list of ingredients, and the model needs to generate 3 recipes based on those ingredients. 
            For each recipe output the recipes in the following JSON format:

            {
            "name": "<Recipe Name>",
            "ingredients": [
                "<Ingredient 1>",
                "<Ingredient 2>",
                ...
            ],
            "instructions": "<Step-by-step instructions>"
            }
            Dont write anything before and after JSON. Only give the JSON output.
            DONT GIVE ANY CODE OR PYTHON SOLUTION. Just give the recipes output in the JSON format.
            Provide the output in the specified JSON format.
            The output should be purely in the JSON format, like the example above.
            Return your output in the JSON format after processing the following ingredients:
        """
        prompt = prompt + ingredients
        response = ollama.generate(model, prompt)
        json_response = json.loads(response.response)
        return render_template('recipe.html', response=json_response)
    return render_template('recipe.html') 


@recipe_bp.route('/saved-recipes', methods=['GET'])
def saved_recipes():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM recipes")
        recipes = cursor.fetchall()
        user = session.get('user')
        return render_template ('saved-recipes.html', recipes=recipes, user=user)