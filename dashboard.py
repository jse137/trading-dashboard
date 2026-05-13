import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Trading Dashboard",
    layout="wide"
)

st.title("📈 Trading Dashboard")

# =========================
# CARGAR CSV
# =========================

try:
    df = pd.read_csv("signals_log.csv")

except:
    st.warning("No existe signals_log.csv")
    st.stop()

# =========================
# TABLA
# =========================

st.subheader("📋 Historial de señales")

st.dataframe(df)

# =========================
# ESTADISTICAS
# =========================

st.subheader("📊 Estadísticas")

total_signals = len(df)

buy_signals = len(df[df['signal'] == 'COMPRA'])
sell_signals = len(df[df['signal'] == 'VENTA'])

col1, col2, col3 = st.columns(3)

col1.metric("Total señales", total_signals)
col2.metric("Compras", buy_signals)
col3.metric("Ventas", sell_signals)

# =========================
# GRAFICO ACTIVOS
# =========================

st.subheader("📈 Señales por activo")

ticker_counts = df['ticker'].value_counts()

fig, ax = plt.subplots()

ticker_counts.plot(
    kind='bar',
    ax=ax
)

st.pyplot(fig)

# =========================
# PRECIOS EN VIVO
# =========================

st.subheader("💹 Mercado actual")

tickers = [
    "YPFD.BA",
    "VIST.BA",
    "JPM.BA"
    "BRKB.BA"
]

market_data = []

for ticker in tickers:

    try:

        data = yf.download(
            ticker,
            period="1d",
            interval="1h",
            auto_adjust=True
        )

        data.columns = data.columns.get_level_values(0)

        last_price = round(
            data['Close'].iloc[-1],
            2
        )

        market_data.append([
            ticker,
            last_price
        ])

    except:
        pass

market_df = pd.DataFrame(
    market_data,
    columns=["Ticker", "Precio"]
)

st.dataframe(market_df)

# =========================
# ULTIMAS SEÑALES
# =========================

st.subheader("🚨 Últimas señales")

st.dataframe(df.tail(10))