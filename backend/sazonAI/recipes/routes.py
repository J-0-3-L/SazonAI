from flask_restx import Resource, Namespace
from flask import request
from google import genai

api = Namespace('recipes',description='Operacion de recetas')

client = genai.Client(api_key='YOUR_API_KEY')

generate_recipes = []

@api.route('/')
class RecipesResource(Resource):
    
    def post(self):
        ingredients = request.get_json()

        if not ingredients or len(ingredients)==0:
            return {'message': 'Ingrese el ingrediente'}, 400

        ingredients_limit = ingredients[:10]
        ingredients_str = ", ".join(ingredients_limit)

        prompt = f"Generame recetas con estos ingredientes: {ingredients_str}"

        response = client.models.generate_content(
            model = 'gemini-2.0-flash',
            contents = prompt,
            max_tokens = 150
        )

        recipes = response['choices'][0]['text']
        recipe_list = recipes.split("\n")

        clean_recipes = []

        for recipe in recipe_list:
            recipe_name = recipe.strip()

            clean_recipes.append(recipe_name)

        generate_recipes.append(clean_recipes)

        return {'recipes':clean_recipes}, 201
        
    
    def get(self):
        pass
