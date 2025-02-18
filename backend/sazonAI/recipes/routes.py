from flask_restx import Resource, Namespace
from flask import request
from google import genai

api = Namespace('recipes',description='Operacion de recetas')

client = genai.Client(api_key='YOUR_API_KEY')

@api.route('/')
class RecipesResource(Resource):
    
    def post(self):
        ingredients = request.get_json()
        ingredients_str = ", ".join(ingredients)

        prompt = f"Generame recetas con estos ingredientes: {ingredients_str}"

        response = client.models.generate_content(
            model = 'gemini-2.0-flash',
            contents = prompt
        )

        return response
        
    
    def get(self):
        pass
