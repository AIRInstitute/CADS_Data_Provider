from flask import Flask, Response, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_restx import  Api, fields
import json
from flask_session import Session

from app.config import SWAGGER_AUTHORIZATIONS



class RelationshipField(fields.Raw):
    __schema_type__ = 'object'

    def output(self, key, obj):
        value = self.get_value(obj, key)
        return {
            'type': 'Relationship',
            'value': value
        }

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, RelationshipField):
            return {
                'type': 'Relationship',
                'value': obj.value
            }
        elif isinstance(obj, Response):
            return obj.get_data().decode('utf-8')
        return super(CustomJSONEncoder, self).default(obj)


def create_app():
    from app.smartdatamodel_api import get_models as get_api_models
    from app.api import get_namespaces as get_routes_namespaces
    from app.smartdatamodel_api import get_namespaces as get_api_namespaces
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
    db = SQLAlchemy()
    app.config['SECRET_KEY'] = "your_super_secret_key_here"
    app.config['SESSION_TYPE'] = 'filesystem'
    app.json_encoder = CustomJSONEncoder
    Session(app)
    from app.auth import login_manager
    login_manager.init_app(app)
    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    api = Api(app, version='1.0', title='Agrisync API', description='Agrisync API', doc='/api-docs/', authorizations=SWAGGER_AUTHORIZATIONS)


    for ns in get_routes_namespaces():
        api.add_namespace(ns)

    for ns in get_api_namespaces():
        api.add_namespace(ns, path="/api")

    for name, model in get_api_models().items():
        api.models[name] = model

    from app.smartdatamodel_api import smartdata_blueprint
    app.register_blueprint(smartdata_blueprint, url_prefix='/api')

    from app.api  import api_blueprint
    app.register_blueprint(api_blueprint)


    '''SWAGGER_URL = "/api-docs"
    API_URL = "/static/swagger.json"
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Agrisync API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)'''
    return app
