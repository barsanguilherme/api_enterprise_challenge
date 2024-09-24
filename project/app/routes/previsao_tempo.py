import json
from flask import Blueprint, request, jsonify
from app.utils.date_utils import get_date_param
import subprocess

previsao_tempo_bp = Blueprint('previsao_tempo', __name__)

@previsao_tempo_bp.route('/previsao_tempo', methods=['GET'])
def get_previsao_tempo():
    """
    Retorna a previsão do tempo para uma data específica.

    ---
    parameters:
      - name: date
        in: query
        type: string
        required: true
        description: Data para qual deseja obter a previsão do tempo (no formato yyyy-MM-dd).
    responses:
      200:
        description: Previsão do tempo para a data fornecida
        examples:
          application/json: 
            {"data": "2024-09-22", "previsao": "Chuva leve", "temperatura": "25ºC"}
      400:
        description: Parâmetro date não fornecido ou inválido
    """
    date = get_date_param(request)
    if not date:
        return jsonify({"error": "Parâmetro 'date' é obrigatório ou está em formato inválido (use yyyy-MM-dd)."}), 400

    url = "http://elasticgrupogpt.pagekite.me/dados_meterologicos_de_previsao_do_tempo/_search"
    username = "elastic"
    password = "HAJhdvYdi2iJTmzUyYI9"

    

    curl_command = [
        'curl',
        '-u', 'elastic:HAJhdvYdi2iJTmzUyYI9',
        '-X', 'GET',
        'http://elasticgrupogpt.pagekite.me/dados_meterologicos_de_previsao_do_tempo/_search',
        '-H', 'Content-Type: application/json',
        '-d', ('{"query": {"exists": {"field": \"' + f"{date}*" + '\"}}}')
    ]

    # Execute the curl command
    result = subprocess.run(curl_command, capture_output=True, text=True)

    # Print the output and any errors

    previsao = json.loads(result.stdout)
    previsoes : list = [prev["_source"] for prev in previsao["hits"]["hits"]]
    return jsonify(previsoes), 200
