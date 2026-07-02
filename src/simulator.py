import pandas as pd


def load_historical(path="data/raw/historical.csv"):
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
    dividends_df,
    usd_rate,
    initial_capital=100000.0,
    monthly_amount=20000.0,
    allocation=None,
    reinvest_dividends=True
):
    """
    Simula una estrategia Dollar Cost Averaging (DCA) incorporando cobro y reinversión de dividendos.

    Parameters
    ----------
    historical : DataFrame
        Histórico de precios.
    dividends_df : DataFrame
        Histórico de dividendos.
    usd_rate : float
        Tipo de cambio USD/ARS de referencia.
    initial_capital : float
        Capital inicial invertido el primer mes.
    monthly_amount : float
        Aporte regular cada mes.
    allocation : dict
        Distribución de la cartera.
    reinvest_dividends : bool
        Si es True, los dividendos se reinvierten automáticamente.

    Returns
    -------
    DataFrame
    """
    if allocation is None:
        allocation = {ticker: 1.0 / len(historical["Ticker"].unique()) for ticker in historical["Ticker"].unique()}

    # Agrupar precios históricos por mes
    monthly_prices = get_monthly_prices(historical)
    monthly_prices["Fecha"] = pd.to_datetime(monthly_prices["Fecha"])
    monthly_prices["AñoMes"] = monthly_prices["Fecha"].dt.to_period("M")

    # Preparar el dataframe de dividendos
    divs = dividends_df.copy()
    divs["Fecha"] = pd.to_datetime(divs["Fecha"])
    divs["AñoMes"] = divs["Fecha"].dt.to_period("M")

    # Ordenar meses cronológicamente
    months = sorted(monthly_prices["AñoMes"].unique())

    accumulated_shares = {ticker: 0.0 for ticker in allocation}
    invested_capital = {ticker: 0.0 for ticker in allocation}

    total_divs_collected_usd = 0.0
    cash_dividends_held_ars = 0.0

    rows = []

    for m in months:
        # 1. Aporte mensual (y capital inicial en el primer mes)
        is_first_month = (m == months[0])
        monthly_contribution = monthly_amount
        if is_first_month:
            monthly_contribution += initial_capital

        # Dinero en efectivo disponible para la compra de este mes
        cash_to_invest = monthly_contribution

        # Obtener los precios de este mes
        prices_this_month = monthly_prices[monthly_prices["AñoMes"] == m]
        if prices_this_month.empty:
            continue

        # Fecha representativa de este mes (último día hábil disponible)
        rep_date = prices_this_month["Fecha"].max()

        # 2. Compra regular
        for ticker in allocation:
            ticker_data = prices_this_month[prices_this_month["Ticker"] == ticker]
            if ticker_data.empty:
                last_available = monthly_prices[(monthly_prices["AñoMes"] <= m) & (monthly_prices["Ticker"] == ticker)]
                if not last_available.empty:
                    price = last_available.sort_values("Fecha").iloc[-1]["Cierre"]
                else:
                    continue
            else:
                price = ticker_data.iloc[0]["Cierre"]

            amount_to_invest = cash_to_invest * allocation[ticker]
            shares_bought = amount_to_invest / price
            accumulated_shares[ticker] += shares_bought
            invested_capital[ticker] += amount_to_invest

        # 3. Cobra dividendos en este mes
        divs_this_month = divs[divs["AñoMes"] == m]
        for _, div_row in divs_this_month.iterrows():
            ticker = div_row["Ticker"]
            if ticker not in allocation:
                continue

            div_usd = div_row["DividendoUSD"]
            shares_held = accumulated_shares[ticker]

            if shares_held > 0:
                received_usd = shares_held * div_usd
                received_ars = received_usd * usd_rate
                total_divs_collected_usd += received_usd

                # 4. Si reinvierte: compra más inmediatamente
                if reinvest_dividends:
                    ticker_data = prices_this_month[prices_this_month["Ticker"] == ticker]
                    if ticker_data.empty:
                        last_available = monthly_prices[(monthly_prices["AñoMes"] <= m) & (monthly_prices["Ticker"] == ticker)]
                        if not last_available.empty:
                            price = last_available.sort_values("Fecha").iloc[-1]["Cierre"]
                        else:
                            price = 1.0
                    else:
                        price = ticker_data.iloc[0]["Cierre"]

                    shares_from_div = received_ars / price
                    accumulated_shares[ticker] += shares_from_div
                else:
                    cash_dividends_held_ars += received_ars

        # 5. Guardar estado de este mes
        portfolio_value = 0.0
        annualized_divs_ars = 0.0

        for ticker in allocation:
            ticker_data = prices_this_month[prices_this_month["Ticker"] == ticker]
            if ticker_data.empty:
                last_available = monthly_prices[(monthly_prices["AñoMes"] <= m) & (monthly_prices["Ticker"] == ticker)]
                price = last_available.sort_values("Fecha").iloc[-1]["Cierre"] if not last_available.empty else 0.0
            else:
                price = ticker_data.iloc[0]["Cierre"]

            portfolio_value += accumulated_shares[ticker] * price

            # Calcular dividendo anualizado de este ticker en este mes m (suma de últimos 12 meses)
            ticker_divs_12m = divs[(divs["Ticker"] == ticker) &
                                   (divs["AñoMes"] > (m - 12)) &
                                   (divs["AñoMes"] <= m)]
            ann_div_usd = ticker_divs_12m["DividendoUSD"].sum()
            annualized_divs_ars += accumulated_shares[ticker] * ann_div_usd * usd_rate

        current_value = portfolio_value + cash_dividends_held_ars
        total_invested = sum(invested_capital.values())
        profit = current_value - total_invested
        performance = (profit / total_invested * 100) if total_invested > 0 else 0.0
        yoc = (annualized_divs_ars / total_invested * 100) if total_invested > 0 else 0.0
        total_shares = sum(accumulated_shares.values())

        rows.append({
            "Fecha": rep_date.strftime("%Y-%m-%d"),
            "CapitalInvertido": round(total_invested, 2),
            "ValorActual": round(current_value, 2),
            "DividendosCobradosUSD": round(total_divs_collected_usd, 4),
            "CEDEARsAcumulados": round(total_shares, 6),
            "YieldOnCost%": round(yoc, 2),
            "Ganancia": round(profit, 2),
            "Rendimiento%": round(performance, 2)
        })

    return pd.DataFrame(rows)