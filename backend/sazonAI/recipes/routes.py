from flask_restx import Resource, Namespace

api = Namespace('recipes',description='Operacion de recetas')

@api.route('/')
class RecipesResource(Resource):
    
    def post(self):

        pass

    def get(self):
        pass
