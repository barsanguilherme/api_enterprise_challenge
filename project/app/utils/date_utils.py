import re
from datetime import datetime

def validate_date(date_string):
    """Valida o formato da data como yyyy-MM-dd."""
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return re.match(pattern, date_string) is not None

def get_date_param(request):
    """Retorna a data passada como parâmetro ou a data atual no formato yyyy-MM-dd."""
    date = request.args.get('date')
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    elif not validate_date(date):
        return None  # Data inválida
    return date
