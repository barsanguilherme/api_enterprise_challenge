from flask import Flask, jsonify
import requests
from requests.auth import HTTPBasicAuth

# Configurações do Flask
app = Flask(__name__)

# URLs dos índices no Elasticsearch
ALAGAMENTOS_INDEX_URL = 'https://elasticgrupogpt.pagekite.me/alagamentos/_search'
PREVISAO_TEMPO_INDEX_URL = 'https://elasticgrupogpt.pagekite.me/dados_meterologicos_de_previsao_do_tempo/_search'

# Credenciais de autenticação para Elasticsearch
ELASTICSEARCH_USERNAME = 'elastic'
ELASTICSEARCH_PASSWORD = 'HAJhdvYdi2iJTmzUyYI9'

# Função para realizar requisição autenticada ao Elasticsearch
def fetch_data_from_elasticsearch(url):
    """Faz uma requisição HTTP ao Elasticsearch e retorna os dados."""
    try:
        response = requests.get(
            url, 
            auth=HTTPBasicAuth(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD), 
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        return {'error': str(error)}

# Endpoint para dados de alagamentos
@app.route('/alagamentos', methods=['GET'])
def fetch_alagamentos_data():
    """Busca e retorna os dados de alagamentos do Elasticsearch."""
    alagamentos_data = fetch_data_from_elasticsearch(ALAGAMENTOS_INDEX_URL)
    return jsonify(alagamentos_data), 200

# Endpoint para dados de previsão do tempo
@app.route('/previsao_tempo', methods=['GET'])
def fetch_weather_forecast_data():
    """Busca e retorna os dados de previsão do tempo do Elasticsearch."""
    previsao_tempo_data = fetch_data_from_elasticsearch(PREVISAO_TEMPO_INDEX_URL)
    return jsonify(previsao_tempo_data), 200

# Executa a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)







