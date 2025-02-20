from flask_restx import Resource, Namespace, fields
from flask import request
from google import genai

api = Namespace('recipes',description='Operacion de recetas')

recipe_model = api.model('Recipe',{
    'name': fields.String(required=True)
})

client = genai.Client(api_key='YOUR_API_KEY')

generate_recipes = []

@api.route('/')
class RecipesResource(Resource):


    @api.marshal_with(recipe_model)
    @api.expect(recipe_model)
    def post(self):
        ingredients = request.get_json()

        if not ingredients or len(ingredients)==0:
            return {'message': 'Ingrese el ingrediente'}, 400

        if isinstance(ingredients, str):
            ingredients = [ingredients]

        if isinstance(ingredients, list):
            ingredients_limit = ingredients[:10]
        else:
            return {'message':'Los ingredientes deben ser una lista o una cadena de texto'}

        #ingredients_limit = ingredients[:10]
        ingredients_str = ", ".join(ingredients_limit)

        prompt = f"Generame recetas con estos ingredientes: {ingredients_str}"

        response = client.models.generate_content(
            model = 'gemini-2.0-flash',
            contents = prompt,
            max_tokens = 150
        )

        recipes = response['choices'][0]['text']
        recipe_list = recipes.split("\n")
        print(recipe_list)

        clean_recipes = []

        for recipe in recipe_list:
            recipe_name = recipe.strip()
            if recipe_name:
                clean_recipes.append({'name':recipe_name})

        #print(clean_recipes)    
        generate_recipes.append(clean_recipes)

        return {'recipes':clean_recipes}, 201
        
    
    def get(self):
        
        return {'recipes': generate_recipes}, 200
