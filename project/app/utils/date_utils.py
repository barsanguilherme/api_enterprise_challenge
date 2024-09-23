import re
from datetime import datetime

def validate_date(date_string):
    """Valida o formato da data como yyyy-MM-dd."""
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return re.match(pattern, date_string) is not None

def get_date_param(request):
    """Retorna a data passada como parâmetro ou uma mensagem de erro se a data for inválida."""
    date = request.args.get('date')
    
    # Verifica se a data foi fornecida
    if not date:
        # Retorna a data atual no formato yyyy-MM-dd
        date = datetime.now().strftime('%Y-%m-%d')
    
    # Valida o formato da data fornecida
    elif not validate_date(date):
        return "Data inválida"  # Retorna mensagem de data inválida
    
    return date  # Retorna a data válida

