from flask import Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
 
# Configurações do Flask
app = Flask(__name__)
 
# URLs dos índices no Elasticsearch
ALAGAMENTOS_INDEX_URL = 'https://elasticgrupogpt.pagekite.me/alagamentos/_search'
PREVISAO_TEMPO_INDEX_URL = 'https://elasticgrupogpt.pagekite.me/dados_meterologicos_de_previsao_do_tempo/_search'
 
# Credenciais de autenticação para Elasticsearch
ELASTICSEARCH_USERNAME = 'elastic'
ELASTICSEARCH_PASSWORD = 'HAJhdvYdi2iJTmzUyYI9'
 
# Função para realizar requisição autenticada ao Elasticsearch com filtro de data
def fetch_data_from_elasticsearch(url, date):
    """Faz uma requisição HTTP ao Elasticsearch e retorna os dados filtrados pela data."""

    query = {
        "query": {
            "exists": {
                "field": date
            }
        }
    }

    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
            json=query,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        return {'error': str(error)}
 
# Função para obter a data passada como parâmetro ou a data atual
def get_date_param():
    """Retorna a data passada como parâmetro ou a data atual no formato yyyy-MM-dd."""
    date = request.args.get('date')
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    return date
 
# Endpoint para dados de alagamentos
@app.route('/alagamentos', methods=['GET'])
def fetch_alagamentos_data():
    """Busca e retorna os dados de alagamentos filtrados pela data."""
    date = get_date_param()
    alagamentos_data = fetch_data_from_elasticsearch(ALAGAMENTOS_INDEX_URL, date)
    return jsonify(alagamentos_data), 200
 
# Endpoint para dados de previsão do tempo
@app.route('/previsao_tempo', methods=['GET'])
def fetch_weather_forecast_data():
    """Busca e retorna os dados de previsão do tempo filtrados pela data."""
    date = get_date_param()
    date = date + "*"
    previsao_tempo_data = fetch_data_from_elasticsearch(PREVISAO_TEMPO_INDEX_URL, date)
    return jsonify(previsao_tempo_data["hits"]["hits"][0]["_source"]), 200
 
# Executa a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)