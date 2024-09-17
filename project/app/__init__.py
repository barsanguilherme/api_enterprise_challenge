from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    # Configuração personalizada do Swagger
    swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # tudo dentro
            "model_filter": lambda tag: True,  # tudo dentro
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "info": {
        "title": "Energy Guard API",
        "description": "API para monitoramento de alagamentos e previsão do tempo, além de interrupções.",
        "version": "0.1"
    },
    "ui_locales": "pt"  # Aqui você especifica o idioma como português
    }
    
    swagger = Swagger(app, config=swagger_config)

    # Importar e registrar os Blueprints
    from .routes.alagamentos import alagamentos_bp
    from .routes.previsao_tempo import previsao_tempo_bp
    from .routes.interrupcoes import interrupcoes_bp  # Importar o novo blueprint

    app.register_blueprint(alagamentos_bp)
    app.register_blueprint(previsao_tempo_bp)
    app.register_blueprint(interrupcoes_bp)  # Registrar o novo blueprint


    return app




