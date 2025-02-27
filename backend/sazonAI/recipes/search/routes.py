from flask_restx import Resource, Namespace, fields
from flask import request
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

api = Namespace('recipes',description='Operacion de recetas')

ingredient_model = api.model('Ingredient',{
    'ingredient': fields.String(required=True),
    'ingredients': fields.List(fields.String, required=True)
})

recipe_model = api.model('Recipes', {
    'recipes': fields.List(fields.Nested(api.model('Recipe', {
        'recipe': fields.String(required=True)})
    ))
})

api_key = os.getenv('YOUR_API_KEY')

client = genai.Client(api_key=api_key)

generate_recipes = []

@api.route('/')
class RecipesResource(Resource):


    @api.marshal_with(recipe_model)
    @api.expect(ingredient_model)
    def post(self):
               
        data = request.get_json()
        if isinstance(data, dict):
            if 'ingredients' in data:
                ingredients = data['ingredients']
            elif 'ingredient' in data:
                ingredients = [data['ingredient']]
            else:
                return {'message': 'Debe enviar al menos un ingrediente'}, 400
        elif isinstance(data, str):
            ingredients = [data]
        else:
            return {'message': 'Formato de datos incorrecto'}, 400

        ingredients_limit = ingredients[:10]
        ingredients_str = ", ".join(ingredients_limit)

        prompt = f"Genera 10 recetas mencionando solo el nombre,sin encabezados, sin enumeraciones , sin descripciones, detalles ni sugerencias, con los siguientes ingredientes: {ingredients_str}"

        response = client.models.generate_content(
            model = 'gemini-2.0-flash',
            contents = prompt,
            #max_output_tokens = 150
        )
        
        recipes = response.text
        recipe_list = recipes.split("\n")
              
        clean_recipes = []

        for recipe in recipe_list:
            recipe_name = recipe.strip()

            if recipe_name:
                clean_recipes.append({'recipe':recipe_name})
 
        generate_recipes.append(clean_recipes)

        return {'message':'ok'}, 200
        
    
    def get(self):
        
        return {'recipes': generate_recipes}, 200
