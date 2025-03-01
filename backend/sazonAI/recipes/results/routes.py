from flask_restx import Namespace, fields, Resource
from flask import request
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

@api.route('/InfoRecipes')
class InfoRecipe(Resource):
    
    def post(self):
        pass


    def get(self):
        pass

