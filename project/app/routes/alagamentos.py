from flask import Blueprint, request, jsonify

alagamentos_bp = Blueprint('alagamentos', __name__)

@alagamentos_bp.route('/alagamentos', methods=['GET'])
def get_alagamentos():
    """
    Retorna as informações sobre alagamentos para uma data específica.
    ---
    parameters:
      - name: data  
        in: query  
        type: string
        required: true
        description: A data para a qual deseja buscar informações sobre alagamentos.
    responses:
      200:
        description: Uma lista de alagamentos para a data fornecida
        examples:
          application/json: 
            {"localizacao": "Rua A", "severidade": "moderado"}
      400:
        description: Parâmetro data não fornecido ou inválido
    """
    date = request.args.get('date')
    if not date:
        return jsonify({"error": "Parâmetro 'date' é obrigatório"}), 400

    alagamentos = {
        "localizacao": "Rua A", "severidade": "moderado",
        "localizacao": "Avenida B", "severidade": "severo"
    }

    return jsonify(alagamentos), 200

