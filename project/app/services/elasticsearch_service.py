import requests
from requests.auth import HTTPBasicAuth

ELASTICSEARCH_USERNAME = 'elastic'
ELASTICSEARCH_PASSWORD = 'HAJhdvYdi2iJTmzUyYI9'

def fetch_data_from_elasticsearch(url, date, is_alagamento=False):
    """Faz uma requisição HTTP ao Elasticsearch e retorna os dados filtrados pela data."""

    query = {
        "query": {
            "match_all" if is_alagamento else "match": {} if is_alagamento else {"data_hora": date}
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
        data = response.json()

        if is_alagamento:
            # Filtra os alagamentos pela data
            filtered_data = [hit['_source'] for hit in data['hits']['hits'] if date in hit['_source']]
            return filtered_data or {'error': 'Nenhum dado encontrado para a data fornecida'}, 404

        if data['hits']['total']['value'] > 0:
            return data['hits']['hits'][0]["_source"], 200
        else:
            return {'error': 'Nenhum dado encontrado para a data fornecida'}, 404

    except requests.exceptions.RequestException as error:
        return {'error': 'Servidor offline', 'details': str(error)}, 500
