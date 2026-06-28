import requests

API_BASE_URL = "https://api.invertironline.com/api/v2"

def get_quote(symbol, access_token, market="bCBA"):
    """
    Obtiene la cotización en tiempo real de un título para un mercado específico.
    """
    url = f"{API_BASE_URL}/{market}/Titulos/{symbol}/Cotizacion"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
