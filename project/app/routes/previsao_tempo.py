from flask import Blueprint, request, jsonify

previsao_tempo_bp = Blueprint('previsao_tempo', __name__)

@previsao_tempo_bp.route('/previsao_tempo', methods=['GET'])
def get_previsao_tempo():
    """
    Retorna a previsão do tempo para uma data específica.
    ---
    parameters:
      - name: data
        in: query
        type: string
        required: true
        description: Data para qual deseja obter a previsão do tempo.
    responses:
      200:
        description: Previsão do tempo para a data fornecida
        examples:
          application/json: 
            {"data": "2024-09-02", "previsao": "Chuva leve", "temperatura": "25ºC"}
      400:
        description: Parâmetro `data` não fornecido ou inválido
    """
    date = request.args.get('date')
    if not date:
        return jsonify({"error": "Parâmetro 'date' é obrigatório"}), 400

    previsao = {
        "data": date,
        "previsao": "Chuva leve",
        "temperatura": "25ºC"
    }

    return jsonify(previsao), 200

