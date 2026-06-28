import pandas as pd


def load_historical(path="data/historical.csv"):
    """
    Carga el histórico de precios.
    """
    df = pd.read_csv(path)

    df["Fecha"] = pd.to_datetime(
        df["Fecha"],
        format="ISO8601"
    )

    return df


def get_monthly_prices(df):
    """
    Obtiene el último precio disponible de cada mes para cada ticker.
    """
    df = df.copy()

    df["AñoMes"] = df["Fecha"].dt.to_period("M")

    monthly = (
        df.sort_values("Fecha")
        .groupby(["Ticker", "AñoMes"])
        .last()
        .reset_index()
    )

    return monthly


def simulate_dca(
    historical,
    monthly_amount,
    allocation
):
    """
    Simula una estrategia Dollar Cost Averaging.

    Parameters
    ----------
    historical : DataFrame
        Histórico de precios.

    monthly_amount : float
        Dinero invertido cada mes.

    allocation : dict
        Ej:
        {
            "MO":0.2,
            "PFE":0.2,
            "T":0.2,
            "CVX":0.2,
            "VALE":0.2
        }

    Returns
    -------
    DataFrame
    """

    monthly_prices = get_monthly_prices(historical)

    rows = []

    accumulated_shares = {
        ticker: 0.0
        for ticker in allocation
    }

    invested_capital = {
        ticker: 0.0
        for ticker in allocation
    }

    for _, row in monthly_prices.iterrows():

        ticker = row["Ticker"]

        if ticker not in allocation:
            continue

        price = row["Cierre"]

        amount = monthly_amount * allocation[ticker]

        shares = amount / price

        accumulated_shares[ticker] += shares

        invested_capital[ticker] += amount

        current_value = accumulated_shares[ticker] * price

        profit = current_value - invested_capital[ticker]

        performance = (
            profit / invested_capital[ticker] * 100
        )

        rows.append({

            "Fecha": row["Fecha"],

            "Ticker": ticker,

            "Precio": round(price, 2),

            "MontoInvertido": round(amount, 2),

            "CEDEARsComprados": round(shares, 6),

            "CEDEARsAcumulados": round(
                accumulated_shares[ticker],
                6
            ),

            "CapitalInvertido": round(
                invested_capital[ticker],
                2
            ),

            "ValorActual": round(
                current_value,
                2
            ),

            "Ganancia": round(
                profit,
                2
            ),

            "Rendimiento%": round(
                performance,
                2
            )

        })

    simulation = pd.DataFrame(rows)

    return simulation


def save_simulation(
    simulation,
    path="data/simulation.csv"
):
    """
    Guarda la simulación en CSV.
    """
    import os

    os.makedirs("data", exist_ok=True)

    simulation.to_csv(
        path,
        index=False
    )