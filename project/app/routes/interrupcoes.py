from flask import Blueprint, request, jsonify

interrupcoes_bp = Blueprint('interrupcoes', __name__)

@interrupcoes_bp.route('/interrupcoes', methods=['GET'])
def get_interrupcoes():
    """
    Retorna as interrupções de energia para uma data específica.
    ---
    parameters:
      - name: data
        in: query
        type: string
        required: true
        description: Data para a qual deseja obter as interrupções de energia no formato YYYY-MM-DD
    responses:
      200:
        description: Lista de interrupções para a data fornecida
        examples:
          application/json:
            [
              {
                "DatGeracaoConjuntoDados": "2024-03-14",
                "IdeConjuntoUnidadeConsumidora": "14236",
                "DscConjuntoUnidadeConsumidora": "TRINDADE",
                "DscAlimentadorSubestacao": "TDD-01C5",
                "DscSubestacaoDistribuicao": "TRINDADE",
                "NumOrdemInterrupcao": "15326228_14086699",
                "DscTipoInterrupcao": "Não Programada",
                "IdeMotivoInterrupcao": "0",
                "DatInicioInterrupcao": "2017-11-29 08:18:37",
                "DatFimInterrupcao": "2017-12-01 08:27:42",
                "DscFatoGeradorInterrupcao": "INTERNO - NAO PROGRAMADA - PROPRIAS DO SISTEMA - FALHA DE MATERIAL OU EQUIPAMENTO",
                "NumNivelTensao": "380",
                "NumUnidadeConsumidora": "1",
                "NumConsumidorConjunto": "36413",
                "NumAno": "2017",
                "NomAgenteRegulado": "COMPANHIA ENERGÉTICA DE PERNAMBUCO",
                "SigAgente": "CELPE",
                "NumCPFCNPJ": "10835932000108"
              }
            ]
      400:
        description: Parâmetro 'data' não fornecido ou inválido
    """
    data = request.args.get('data')
    if not data:
        return jsonify({"error": "Parâmetro 'data' é obrigatório"}), 400

    interrupcoes_exemplo = [
        {
            "DatGeracaoConjuntoDados": "2024-03-14",
            "IdeConjuntoUnidadeConsumidora": "14236",
            "DscConjuntoUnidadeConsumidora": "TRINDADE",
            "DscAlimentadorSubestacao": "TDD-01C5",
            "DscSubestacaoDistribuicao": "TRINDADE",
            "NumOrdemInterrupcao": "15326228_14086699",
            "DscTipoInterrupcao": "Não Programada",
            "IdeMotivoInterrupcao": "0",
            "DatInicioInterrupcao": "2017-11-29 08:18:37",
            "DatFimInterrupcao": "2017-12-01 08:27:42",
            "DscFatoGeradorInterrupcao": "INTERNO - NAO PROGRAMADA - PROPRIAS DO SISTEMA - FALHA DE MATERIAL OU EQUIPAMENTO",
            "NumNivelTensao": "380",
            "NumUnidadeConsumidora": "1",
            "NumConsumidorConjunto": "36413",
            "NumAno": "2017",
            "NomAgenteRegulado": "COMPANHIA ENERGÉTICA DE PERNAMBUCO",
            "SigAgente": "CELPE",
            "NumCPFCNPJ": "10835932000108"
        }
    ]

    interrupcoes_filtradas = [interrupcao for interrupcao in interrupcoes_exemplo if interrupcao["DatGeracaoConjuntoDados"] == data]

    if not interrupcoes_filtradas:
        return jsonify({"error": f"Não foram encontradas interrupções para a data {data}"}), 404

    return jsonify(interrupcoes_filtradas), 200
