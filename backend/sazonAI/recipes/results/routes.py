from flask_restx import Namespace, fields, Resource
from flask import request
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

api_key=os.getenv('YOUR_API_KEY')

client = genai.Client(api_key=api_key)

@api.route('/InfoRecipes')
class InfoRecipe(Resource):
    
    def post(self):

        recipe_name = request.json.get('recipe_name')
        prompt = f"Genera una receta con título, descripción, ingredientes y preparación para la receta: {recipe_name}"

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )

        pass


    def get(self):
        pass

