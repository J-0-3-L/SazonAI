from flask import Flask
from flask_restx import Api


api = Api()

def create_app():

    app = Flask(__name__)

    api = Api(
        app,
        title='SazonAI',
        version='1.0',
        description='SazonAI es un recetarios personalizado que te brinda recetas de acuerdo a las recetas buscadas haciendo uso de una AI',
        doc='/docs'
    )

    with app.app_context():
        
        from sazonAI.recipes.search.routes import api as recipes_api
        api.add_namespace(recipes_api)

    return app



