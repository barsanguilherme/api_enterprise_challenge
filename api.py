from flask import Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import re

# Configurações do Flask
app = Flask(__name__)

# URLs dos índices no Elasticsearch
ALAGAMENTOS_INDEX_URL = 'https://elasticgrupogpt.pagekite.me/alagamentos/_search'
PREVISAO_TEMPO_INDEX_URL = 'https://elasticgrupogpt.pagekite.me/dados_meterologicos_de_previsao_do_tempo/_search'

# Credenciais de autenticação para Elasticsearch
ELASTICSEARCH_USERNAME = 'elastic'
ELASTICSEARCH_PASSWORD = 'HAJhdvYdi2iJTmzUyYI9'

# Função para realizar requisição autenticada ao Elasticsearch
def fetch_data_from_elasticsearch(url, date):
    """Faz uma requisição HTTP ao Elasticsearch e retorna os dados filtrados pela data."""
    
    if "alagamentos" in url:
        query = {
            "query": {
                "match_all": {}
            }
        }
    else:
        # Consulta usando match para tentar buscar dados pela data
        query = {
            "query": {
                "match": {
                    "data_hora": date
                }
            }
        }

    try:
        print(f"Enviando consulta para o Elasticsearch: {query}")  # Log da consulta
        response = requests.get(
            url,
            auth=HTTPBasicAuth(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
            json=query,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        print(f"Resposta do Elasticsearch: {data}")  # Log da resposta

        if "alagamentos" in url:
            # Filtrando os documentos de alagamentos no código com base na data passada
            filtered_data = []
            for hit in data['hits']['hits']:
                for key, value in hit['_source'].items():
                    if date in key:
                        filtered_data.append({key: value})

            if not filtered_data:
                return {'error': 'Nenhum dado encontrado para a data fornecida'}, 404

            return filtered_data, 200
        else:
            # Para previsão do tempo, retornando diretamente os dados
            if data['hits']['total']['value'] > 0:
                return data['hits']['hits'][0]["_source"], 200
            else:
                return {'error': 'Nenhum dado encontrado para a data fornecida'}, 404

    except requests.exceptions.RequestException as error:
        # Se houver erro de conexão com o Elasticsearch, retornamos uma mensagem de erro
        return {'error': 'Servidor offline', 'details': str(error)}, 500

# Função para validar a data no formato yyyy-MM-dd
def validate_date(date_string):
    """Valida o formato da data como yyyy-MM-dd."""
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return re.match(pattern, date_string) is not None

# Função para obter a data passada como parâmetro ou a data atual
def get_date_param():
    """Retorna a data passada como parâmetro ou a data atual no formato yyyy-MM-dd."""
    date = request.args.get('date')
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    elif not validate_date(date):
        return None  # Data inválida
    return date

# Endpoint para dados de alagamentos
@app.route('/alagamentos', methods=['GET'])
def fetch_alagamentos_data():
    """Busca e retorna os dados de alagamentos filtrados pela data."""
    date = get_date_param()
    if date is None:
        # Retorna erro 400 para formato de data inválido
        return jsonify({'error': 'Data inserida no formato errado, use yyyy-MM-dd'}), 400

    alagamentos_data, status_code = fetch_data_from_elasticsearch(ALAGAMENTOS_INDEX_URL, date)
    return jsonify(alagamentos_data), status_code

# Endpoint para dados de previsão do tempo
@app.route('/previsao_tempo', methods=['GET'])
def fetch_weather_forecast_data():
    """Busca e retorna os dados de previsão do tempo filtrados pela data."""
    date = get_date_param()
    if date is None:
        # Retorna erro 400 para formato de data inválido
        return jsonify({'error': 'Data inserida no formato errado, use yyyy-MM-dd'}), 400

    previsao_tempo_data, status_code = fetch_data_from_elasticsearch(PREVISAO_TEMPO_INDEX_URL, date)
    return jsonify(previsao_tempo_data), status_code

# Executa a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)