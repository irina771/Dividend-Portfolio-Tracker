from datetime import date

from src.api import IOLClient
from src.auth import get_access_token
from src.csv_manager import (
    save_quote,
    save_historical,
    save_simulation,
    save_portfolio_metrics,
)
from src.portfolio import (
    load_portfolio,
    load_dividends,
    calculate_portfolio_metrics,
    get_portfolio_summary,
    get_usd_ars_rate,
)
from src.simulator import (
    load_historical,
    simulate_dca,
)

CEDEARS = [
    "MO",
    "PFE",
    "T",
    "CVX",
    "VALE"
]


def main():

    print("=" * 60)
    print("Dividend Portfolio Tracker - Pipeline ETL e Inversion")
    print("=" * 60)

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

    print("=" * 60)
    print("Resumen de Posición de la Cartera (Pesos/ARS)")
    print("=" * 60)

    portfolio = load_portfolio()

    df_metrics = calculate_portfolio_metrics(
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

    for _, row in df_metrics.iterrows():

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

    summary = get_portfolio_summary(df_metrics)

    print(col_fmt.format(
        "TOTAL",
        "",
        f"${summary['costo_total']:,.0f}",
        f"${summary['valor_actual']:,.0f}",
        f"${summary['ganancia_total']:,.0f}",
        f"{summary['rendimiento_total%']}%",
        "100%"
    ))

    # Guardar las métricas de portafolio procesadas
    save_portfolio_metrics(df_metrics)
    print("\nMétricas del portafolio guardadas en: data/processed/portfolio_metrics.csv")

    # ===============================
    # Reporte Detallado de Dividendos
    # ===============================

    print("\n" + "=" * 60)
    print("Reporte Analitico de Dividendos (Dolar de Referencia CCL: ${:,.2f})".format(summary["dolar_ccl"]))
    print("=" * 60)

    col_div_fmt = "{:<6} {:>10} {:>10} {:>12} {:>12} {:>12} {:>12}"
    print(col_div_fmt.format(
        "Ticker",
        "Yield",
        "YOC",
        "Cobrado 24",
        "Cobrado 25",
        "Cobrado 26",
        "Est.Anual"
    ))
    print("-" * 80)

    for _, row in df_metrics.iterrows():
        print(col_div_fmt.format(
            row["Ticker"],
            f"{row['DividendYield%']}%",
            f"{row['YieldOnCost%']}%",
            f"US$ {row['DivsCobrados2024_USD']:,.2f}",
            f"US$ {row['DivsCobrados2025_USD']:,.2f}",
            f"US$ {row['DivsCobrados2026_USD']:,.2f}",
            f"US$ {row['IncomeAnualUSD']:,.2f}"
        ))
    print("-" * 80)
    print(col_div_fmt.format(
        "TOTAL",
        "",
        "",
        f"US$ {summary['total_divs_cobrados_2024_usd']:,.2f}",
        f"US$ {summary['total_divs_cobrados_2025_usd']:,.2f}",
        f"US$ {summary['total_divs_cobrados_2026_usd']:,.2f}",
        f"US$ {summary['total_income_anual_usd']:,.2f}"
    ))
    print("\nIngreso Anual Esperado en ARS: ${:,.2f}".format(summary["total_income_anual_ars"]))

    # ===============================
    # Simulación DCA
    # ===============================

    print("\n" + "=" * 60)
    print("Simulación de Inversión DCA (con Reinversión de Dividendos)")
    print("=" * 60)

    historical_prices = load_historical()
    dividends_df = load_dividends()
    usd_rate = get_usd_ars_rate()

    # Simulación con reinversión activa
    simulation = simulate_dca(
        historical=historical_prices,
        dividends_df=dividends_df,
        usd_rate=usd_rate,
        initial_capital=1000000.0,
        monthly_amount=200000.0,
        allocation={
            "MO": 0.20,
            "PFE": 0.20,
            "T": 0.20,
            "CVX": 0.20,
            "VALE": 0.20,
        },
        reinvest_dividends=True
    )

    save_simulation(simulation)

    print(simulation.tail())

    print("\nSimulación guardada correctamente en:")
    print("data/processed/simulation.csv")


if __name__ == "__main__":
    main()