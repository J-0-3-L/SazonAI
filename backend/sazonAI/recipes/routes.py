from flask_restx import Resource, Namespace
from flask import request

api = Namespace('recipes',description='Operacion de recetas')

@api.route('/')
class RecipesResource(Resource):
    
    def post(self):
        ingredients = request.get_json()
        ingredients_str = ", ".join(ingredients)

        prompt = f"Generame recetas con estos ingredientes: {ingredients_str}"

        response = 
        
    
    def get(self):
        pass
