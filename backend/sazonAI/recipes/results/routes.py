from flask_restx import Namespace, fields, Resource
from flask import request
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

api = Namespace('recipe_info', description='Detalles de una receta')

api_key=os.getenv('YOUR_API_KEY')

client = genai.Client(api_key=api_key)

recipe_info_model = api.model('RecipeInfo', {
    'title': fields.String,
    'description': fields.String,
    'ingredients': fields.List(fields.String),
    'preparation': fields.String
})

@api.route('/InfoRecipes')
class InfoRecipe(Resource):
   
    @api.marshal_with(recipe_info_model)
    def post(self):

        recipe_name = request.json.get('recipe_name')
        #prompt = f"Genera una receta con título, descripción, ingredientes y preparación para la receta: {recipe_name}"

        prompt = (
            f"Genera una receta completa con título, descripción, lista de ingredientes y pasos de preparación "
            f"para el platillo: {recipe_name}. Organiza la respuesta claramente en esos cuatro apartados."
        )

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )

        text = response.text

        lines = text.split('\n')
        title, description, ingredients, preparation = "", "", [], ""
        current_section = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if "título" in line.lower() or line.lower().startswith("titulo:"):
                current_section = "title"
                title = line.split(":", 1)[-1].strip()
            elif "descripción" in line.lower():
                current_section = "description"
            elif "ingredientes" in line.lower():
                current_section = "ingredients"
            elif "preparación" in line.lower() or "instrucciones" in line.lower():
                current_section = "preparation"
            else:
                if current_section == "description":
                    description += line + " "
                elif current_section == "ingredients":
                    ingredients.append(line)
                elif current_section == "preparation":
                    preparation += line + " "

        return {
            'title': title or recipe_name,
            'description': description.strip(),
            'ingredients': ingredients,
            'preparation': preparation.strip()
        }, 200
        

        #pass


    def get(self):
        pass

