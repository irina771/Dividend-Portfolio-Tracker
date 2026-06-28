from datetime import date

from src.api import IOLClient
from src.auth import get_access_token
from src.csv_manager import save_quote, save_historical
from src.portfolio import (
    load_portfolio,
    calculate_portfolio_metrics,
    get_portfolio_summary,
)
from src.simulator import (
    load_historical,
    simulate_dca,
    save_simulation,
)

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

    # ===============================
    # Autenticación
    # ===============================

    token_data = get_access_token()
    token = token_data["access_token"]

    client = IOLClient(token)

    print("Token obtenido correctamente.\n")

    latest_prices = {}

    # ===============================
    # Descarga de datos
    # ===============================

    for ticker in CEDEARS:

        print(f"Consultando {ticker}...")

        quote = client.get_quote(ticker)

        precio = quote["ultimoPrecio"]
        latest_prices[ticker] = precio

        print(f"Precio actual: ${precio:,.2f}")

        save_quote(ticker, quote)

        historical = client.get_historical(
            ticker,
            "2024-01-01",
            date.today().strftime("%Y-%m-%d")
        )

        save_historical(ticker, historical)

        print("Histórico guardado.\n")

    # ===============================
    # Resumen del Portfolio
    # ===============================

    print("=" * 50)
    print("Resumen del Portafolio")
    print("=" * 50)

    portfolio = load_portfolio()

    df = calculate_portfolio_metrics(
        portfolio,
        latest_prices
    )

    col_fmt = "{:<6} {:>10} {:>12} {:>12} {:>10} {:>10} {:>8}"

    print(col_fmt.format(
        "Ticker",
        "Cantidad",
        "Costo Tot.",
        "Valor Act.",
        "Ganancia",
        "Rend.%",
        "Peso%"
    ))

    print("-" * 72)

    for _, row in df.iterrows():

        print(col_fmt.format(
            row["Ticker"],
            int(row["Cantidad"]),
            f"${row['CostoTotal']:,.0f}",
            f"${row['ValorActual']:,.0f}",
            f"${row['Ganancia']:,.0f}",
            f"{row['Rendimiento%']}%",
            f"{row['Peso%']}%"
        ))

    print("-" * 72)

    summary = get_portfolio_summary(df)

    print(col_fmt.format(
        "TOTAL",
        "",
        f"${summary['costo_total']:,.0f}",
        f"${summary['valor_actual']:,.0f}",
        f"${summary['ganancia_total']:,.0f}",
        f"{summary['rendimiento_total%']}%",
        "100%"
    ))

    # ===============================
    # Simulación DCA
    # ===============================

    print("\n" + "=" * 50)
    print("Simulación de Inversión")
    print("=" * 50)

    historical = load_historical()

    simulation = simulate_dca(
        historical=historical,
        monthly_amount=200000,
        allocation={
            "MO": 0.20,
            "PFE": 0.20,
            "T": 0.20,
            "CVX": 0.20,
            "VALE": 0.20,
        }
    )

    save_simulation(simulation)

    print(simulation.tail())

    print("\nSimulación guardada correctamente en:")
    print("data/simulation.csv")


if __name__ == "__main__":
    main()