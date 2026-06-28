import requests

API_BASE_URL = "https://api.invertironline.com/api/v2"


class IOLClient:

    def __init__(self, access_token):
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def get_quote(self, symbol, market="bCBA"):
        url = f"{API_BASE_URL}/{market}/Titulos/{symbol}/Cotizacion"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json()

    def get_historical(
        self,
        symbol,
        start_date,
        end_date,
        market="bCBA"
    ):
        url = (
            f"{API_BASE_URL}/"
            f"{market}/Titulos/"
            f"{symbol}/Cotizacion/"
            f"seriehistorica/"
            f"{start_date}/"
            f"{end_date}/"
            f"sinAjustar"
        )

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json()