import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Trading Dashboard",
    layout="wide"
)

st.title("📈 Trading Dashboard")

st.markdown("""
<style>

.big-font {
    font-size:22px !important;
    font-weight:bold;
}

.green {
    color:#00cc66;
}

.red {
    color:#ff4b4b;
}

.yellow {
    color:#ffcc00;
}

</style>
""", unsafe_allow_html=True)

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

st.subheader("🧠 IA MARKET STATUS")

latest_score = 7.5

if latest_score >= 8:

    st.success("🟢 COMPRA FUERTE")

elif latest_score >= 5:

    st.warning("🟡 ESPERAR")

else:

    st.error("🔴 VENTA / DEBILIDAD")

if latest_score >= 8:

    st.markdown(
        '<p class="big-font green">🟢 MERCADO FUERTE</p>',
        unsafe_allow_html=True
    )

elif latest_score >= 5:

    st.markdown(
        '<p class="big-font yellow">🟡 MERCADO NEUTRO</p>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<p class="big-font red">🔴 MERCADO DEBIL</p>',
        unsafe_allow_html=True
    )

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

st.subheader("📈 RSI + PRECIO")

try:

    ticker_chart = "YPFD.BA"

    data = yf.download(
        ticker_chart,
        period="3mo",
        interval="1d",
        auto_adjust=True
    )

    data.columns = data.columns.get_level_values(0)

    # RSI

    delta = data['Close'].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    # GRAFICO PLOTLY

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name='Precio'
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=rsi,
        mode='lines',
        name='RSI'
    ))

    fig.update_layout(
        height=600,
        template='plotly_dark',
        title=f"{ticker_chart} - Precio + RSI"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

except:
    st.warning("No se pudo cargar gráfico")

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

st.subheader("🏆 Ranking de activos")

ranking = df['ticker'].value_counts()

st.dataframe(ranking)

st.subheader("🚨 Últimas señales")

st.dataframe(df.tail(10))