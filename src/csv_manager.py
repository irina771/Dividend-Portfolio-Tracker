import os
from datetime import datetime

import pandas as pd


CSV_PATH = "data/prices.csv"


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

    os.makedirs("data", exist_ok=True)

    if os.path.exists(CSV_PATH):

        df.to_csv(
            CSV_PATH,
            mode="a",
            index=False,
            header=False
        )

    else:

        df.to_csv(
            CSV_PATH,
            index=False
        )