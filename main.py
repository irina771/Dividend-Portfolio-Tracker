from src.auth import get_access_token
from src.api import get_quote
from src.csv_manager import save_quote


CEDEARS = [
    "MO",
    "PFE",
    "T",
    "CVX",
    "VALE"
]


def main():

    print("=" * 50)
    print("Dividend Portfolio Tracker")
    print("=" * 50)

    token_data = get_access_token()
    token = token_data["access_token"]

    print("Token obtenido correctamente\n")

    for ticker in CEDEARS:

        print(f"Consultando {ticker}...")

        quote = get_quote(ticker, token)

        print(f"Precio: ${quote['ultimoPrecio']}")

        save_quote(ticker, quote)

        print("Guardado correctamente\n")


if __name__ == "__main__":
    main()