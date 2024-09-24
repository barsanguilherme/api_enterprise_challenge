import requests
from requests.auth import HTTPBasicAuth

ELASTICSEARCH_USERNAME = 'elastic'
ELASTICSEARCH_PASSWORD = 'HAJhdvYdi2iJTmzUyYI9'

def fetch_data_from_elasticsearch(url, date, is_alagamento=False):
    """Faz uma requisição HTTP ao Elasticsearch e retorna os dados filtrados pela data."""

    # Ajusta a query conforme o tipo de dado (alagamento ou não)
    query = {
        "query": {
            "match": {
                "data_hora": date
            }
        }
    }

    if is_alagamento:
        query = {
            "query": {
                "match": {
                    "data_alagamento": date  # Supondo que "data_alagamento" seja o campo correto para alagamentos
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
        data = response.json()

        if is_alagamento:
            # Filtra os alagamentos pela data
            filtered_data = [hit['_source'] for hit in data['hits']['hits'] if date in hit['_source'].get('data_alagamento', '')]
            if filtered_data:
                return filtered_data, 200
            return {'error': 'Nenhum dado encontrado para a data fornecida'}, 404

        # Caso não seja alagamento, retornamos o primeiro resultado (ou todos conforme a necessidade)
        if data['hits']['total']['value'] > 0:
            return data['hits']['hits'][0]["_source"], 200
        else:
            return {'error': 'Nenhum dado encontrado para a data fornecida'}, 404

    except requests.exceptions.RequestException as error:
        return {'error': 'Servidor offline', 'details': str(error)}, 500
