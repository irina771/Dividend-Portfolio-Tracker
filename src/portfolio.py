import os
import pandas as pd
import requests

PORTFOLIO_CSV = "data/processed/portfolio.csv"
DIVIDENDS_CSV = "data/raw/dividends.csv"


def get_usd_ars_rate():
    """
    Obtiene el tipo de cambio de referencia (Contado con Liquidación)
    desde dolarapi.com con fallback ante fallos.
    """
    try:
        response = requests.get("https://dolarapi.com/v1/dolares/contadoconliqui", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return float(data.get("venta", 1300.0))
    except Exception:
        pass
    return 1300.0


def load_portfolio():
    """
    Carga el portafolio desde el CSV procesado.
    Retorna un DataFrame con columnas: Ticker, Cantidad, PrecioCompra.
    """
    return pd.read_csv(PORTFOLIO_CSV)


def load_dividends():
    """
    Carga el historial de dividendos desde el CSV crudo.
    """
    if os.path.exists(DIVIDENDS_CSV):
        df = pd.read_csv(DIVIDENDS_CSV)
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        return df
    return pd.DataFrame(columns=["Ticker", "Fecha", "DividendoUSD"])


def calculate_portfolio_metrics(portfolio: pd.DataFrame, latest_prices: dict) -> pd.DataFrame:
    """
    Calcula métricas financieras y de dividendos para cada posición de la cartera.
    """
    df = portfolio.copy()
    usd_rate = get_usd_ars_rate()
    divs_df = load_dividends()

    # Precios y costos
    df["PrecioActual"] = df["Ticker"].map(latest_prices)
    df["CostoTotal"] = df["Cantidad"] * df["PrecioCompra"]
    df["ValorActual"] = df["Cantidad"] * df["PrecioActual"]
    df["Ganancia"] = df["ValorActual"] - df["CostoTotal"]
    df["GananciaPorAccion"] = (df["PrecioActual"] - df["PrecioCompra"]).round(2)
    df["Rendimiento%"] = (df["Ganancia"] / df["CostoTotal"] * 100).round(2)

    total_valor = df["ValorActual"].sum()
    df["Peso%"] = (df["ValorActual"] / total_valor * 100).round(2)

    # Métricas de dividendos
    divs_anuales = []
    divs_2024 = []
    divs_2025 = []
    divs_2026 = []
    total_divs_list = []

    for _, row in df.iterrows():
        ticker = row["Ticker"]
        qty = row["Cantidad"]

        ticker_divs = divs_df[divs_df["Ticker"] == ticker]

        # Dividendos anuales (últimos 365 días del último dividendo registrado)
        if not ticker_divs.empty:
            latest_date = ticker_divs["Fecha"].max()
            start_date = latest_date - pd.Timedelta(days=365)
            recent_divs = ticker_divs[(ticker_divs["Fecha"] > start_date) & (ticker_divs["Fecha"] <= latest_date)]
            ann_div = recent_divs["DividendoUSD"].sum()
        else:
            ann_div = 0.0

        divs_anuales.append(ann_div)

        # Cobrados por año
        cobr_2024 = ticker_divs[ticker_divs["Fecha"].dt.year == 2024]["DividendoUSD"].sum() * qty
        cobr_2025 = ticker_divs[ticker_divs["Fecha"].dt.year == 2025]["DividendoUSD"].sum() * qty
        cobr_2026 = ticker_divs[ticker_divs["Fecha"].dt.year == 2026]["DividendoUSD"].sum() * qty
        total_cobr = ticker_divs["DividendoUSD"].sum() * qty

        divs_2024.append(cobr_2024)
        divs_2025.append(cobr_2025)
        divs_2026.append(cobr_2026)
        total_divs_list.append(total_cobr)

    df["DividendoAnualUSD"] = divs_anuales
    df["DivsCobrados2024_USD"] = divs_2024
    df["DivsCobrados2025_USD"] = divs_2025
    df["DivsCobrados2026_USD"] = divs_2026
    df["TotalDivsCobrados_USD"] = total_divs_list

    # Dividend Yield y Yield on Cost
    df["DividendYield%"] = ((df["DividendoAnualUSD"] * usd_rate) / df["PrecioActual"] * 100).round(2)
    df["YieldOnCost%"] = ((df["DividendoAnualUSD"] * usd_rate) / df["PrecioCompra"] * 100).round(2)

    # Ingreso anual esperado
    df["IncomeAnualUSD"] = (df["Cantidad"] * df["DividendoAnualUSD"]).round(2)
    df["IncomeAnualARS"] = (df["Cantidad"] * df["DividendoAnualUSD"] * usd_rate).round(2)

    return df


def get_portfolio_summary(df: pd.DataFrame) -> dict:
    """
    Retorna un resumen del portafolio completo con dividendos.
    """
    costo_total = df["CostoTotal"].sum()
    valor_actual = df["ValorActual"].sum()
    usd_rate = get_usd_ars_rate()

    return {
        "costo_total": costo_total,
        "valor_actual": valor_actual,
        "ganancia_total": df["Ganancia"].sum(),
        "rendimiento_total%": round(((valor_actual - costo_total) / costo_total * 100), 2) if costo_total > 0 else 0.0,
        "dolar_ccl": usd_rate,
        "total_income_anual_usd": df["IncomeAnualUSD"].sum(),
        "total_income_anual_ars": df["IncomeAnualARS"].sum(),
        "total_divs_cobrados_2024_usd": df["DivsCobrados2024_USD"].sum(),
        "total_divs_cobrados_2025_usd": df["DivsCobrados2025_USD"].sum(),
        "total_divs_cobrados_2026_usd": df["DivsCobrados2026_USD"].sum(),
        "total_divs_cobrados_usd": df["TotalDivsCobrados_USD"].sum()
    }
