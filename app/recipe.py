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
    if 'user' not in session:
            return render_template('index.html')
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

@recipe_bp.route('/save-recipe', methods=['POST'])
def save_recipe():
    if 'user' not in session:
        return render_template('index.html')
    connection = create_connection()
    if connection:
        recipe_name = request.form.get('recipe_name')
        recipe_instructions = request.form.get('recipe_instructions')
        recipe_ingredients = request.form.get('recipe_ingredients')
        
        print(recipe_name, recipe_instructions, recipe_ingredients)
        
        cursor = connection.cursor()
        cursor.execute("INSERT INTO recipes (recipe_name, recipe_instructions, recipe_ingredients,  user_id) VALUES (%s, %s, %s, %s)", (recipe_name, recipe_instructions, recipe_ingredients, session.get('user_id')))
        connection.commit()
        return 'Recipe saved successfully'
    return 'Failed to save recipe'


@recipe_bp.route('/saved-recipes', methods=['GET'])
def saved_recipes():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM recipes WHERE user_id = %s", (session.get('user_id'),))
        recipes = cursor.fetchall()
        print(recipes)
        
        user = session.get('user')
        return render_template ('saved-recipes.html', response=recipes, user=user)