from flask import Blueprint, request, jsonify
from app.utils.date_utils import get_date_param

alagamentos_bp = Blueprint('alagamentos', __name__)

@alagamentos_bp.route('/alagamentos', methods=['GET'])
def get_alagamentos():
    """
    Retorna as informações sobre alagamentos para uma data específica.

    ---
    parameters:
      - name: date  
        in: query  
        type: string
        required: true
        description: A data para a qual deseja buscar informações sobre alagamentos (no formato yyyy-MM-dd).
    responses:
      200:
        description: Uma lista de alagamentos para a data fornecida
        examples:
          application/json: 
            [{"localizacao": "Rua A", "severidade": "moderado"},
             {"localizacao": "Avenida B", "severidade": "severo"}]
      400:
        description: Parâmetro data não fornecido ou inválido
    """
    date = get_date_param(request)
    if not date:
        return jsonify({"error": "Parâmetro 'date' é obrigatório ou está em formato inválido (use yyyy-MM-dd)."}), 400

    # Simulação de dados de alagamento
    alagamentos = [
        {"localizacao": "Rua A", "severidade": "moderado"},
        {"localizacao": "Avenida B", "severidade": "severo"}
    ]

    return jsonify(alagamentos), 200
