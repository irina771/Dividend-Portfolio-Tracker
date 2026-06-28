import pandas as pd

PORTFOLIO_CSV = "data/portfolio.csv"

def load_portfolio():
    """
    Carga el portafolio desde el CSV estático.
    Retorna un DataFrame con columnas: Ticker, Cantidad, PrecioCompra.
    """
    return pd.read_csv(PORTFOLIO_CSV)


def calculate_portfolio_metrics(portfolio: pd.DataFrame, latest_prices: dict) -> pd.DataFrame:
    """
    Calcula métricas para cada posición del portafolio.

    Args:
        portfolio: DataFrame con columnas Ticker, Cantidad, PrecioCompra.
        latest_prices: dict {ticker: precio_actual}.

    Returns:
        DataFrame enriquecido con ValorActual, CostoTotal, Ganancia, Rendimiento (%), Peso (%).
    """
    df = portfolio.copy()

    df["PrecioActual"] = df["Ticker"].map(latest_prices)

    df["CostoTotal"] = df["Cantidad"] * df["PrecioCompra"]
    df["ValorActual"] = df["Cantidad"] * df["PrecioActual"]

    df["Ganancia"] = df["ValorActual"] - df["CostoTotal"]

    df["GananciaPorAccion"] = (
        df["PrecioActual"] - df["PrecioCompra"]
    ).round(2)

    df["Rendimiento%"] = (
        df["Ganancia"] / df["CostoTotal"] * 100
    ).round(2)

    total_valor = df["ValorActual"].sum()

    df["Peso%"] = (
        df["ValorActual"] / total_valor * 100
    ).round(2)

    return df


def get_portfolio_summary(df: pd.DataFrame) -> dict:
    """
    Retorna un resumen del portafolio completo.
    """
    return {
        "costo_total": df["CostoTotal"].sum(),
        "valor_actual": df["ValorActual"].sum(),
        "ganancia_total": df["Ganancia"].sum(),
        "rendimiento_total%": round(
            (df["ValorActual"].sum() - df["CostoTotal"].sum()) / df["CostoTotal"].sum() * 100, 2
        )
    }
