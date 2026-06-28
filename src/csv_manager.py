import os
from datetime import datetime

import pandas as pd

PRICES_CSV = "data/prices.csv"
HISTORICAL_CSV = "data/historical.csv"


def save_quote(symbol, quote):

    row = {
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Ticker": symbol,
        "UltimoPrecio": quote.get("ultimoPrecio"),
        "Variacion": quote.get("variacionPorcentual"),
        "Apertura": quote.get("apertura"),
        "Maximo": quote.get("maximo"),
        "Minimo": quote.get("minimo"),
        "Volumen": quote.get("volumenNominal")
    }

    df = pd.DataFrame([row])

    os.makedirs("data/", exist_ok=True)

    if os.path.exists(PRICES_CSV):
        df.to_csv(PRICES_CSV, mode="a", header=False, index=False)
    else:
        df.to_csv(PRICES_CSV, index=False)


def save_historical(symbol, historical_data):

    os.makedirs("data/", exist_ok=True)

    rows = []

    for item in historical_data:

        rows.append({
            "Fecha": item.get("fechaHora"),
            "Ticker": symbol,
            "Apertura": item.get("apertura"),
            "Maximo": item.get("maximo"),
            "Minimo": item.get("minimo"),
            "Cierre": item.get("ultimoPrecio"),
            "Volumen": item.get("volumenNominal")
        })

    df_nuevo = pd.DataFrame(rows)

    if os.path.exists(HISTORICAL_CSV):
        df_existente = pd.read_csv(HISTORICAL_CSV)
        df = pd.concat([df_existente, df_nuevo], ignore_index=True)
    else:
        df = df_nuevo

    df.drop_duplicates(
        subset=["Ticker", "Fecha"],
        keep="last",
        inplace=True
    )

    df.sort_values(
        by=["Ticker", "Fecha"],
        inplace=True
    )

    df.to_csv(HISTORICAL_CSV, index=False)