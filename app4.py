import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from ta.trend import EMAIndicator, SMAIndicator
from ta.volume import VolumeWeightedAveragePrice
import numpy as np

# Função para baixar dados do ticker
def get_data(ticker):
    try:
        data = yf.download(ticker, period='1y', interval='1d')
        return data
    except Exception as e:
        st.error(f"Erro ao baixar dados: {e}")
        return None

# Função para calcular indicadores
def calculate_indicators(data):
    data['EMA_9'] = EMAIndicator(data['Close'], window=9).ema_indicator()
    data['EMA_20'] = EMAIndicator(data['Close'], window=20).ema_indicator()
    data['EMA_50'] = EMAIndicator(data['Close'], window=50).ema_indicator()
    data['EMA_200'] = EMAIndicator(data['Close'], window=200).ema_indicator()
    data['SMA_200'] = SMAIndicator(data['Close'], window=200).sma_indicator()
    data['VWAP'] = VolumeWeightedAveragePrice(high=data['High'], low=data['Low'], close=data['Close'], volume=data['Volume']).volume_weighted_average_price()
    return data

# Função para prever o próximo preço
def predict_next_price(data):
    latest_data = data.iloc[-1]
    price_trend = "alta" if latest_data['EMA_9'] > latest_data['EMA_20'] else "baixa"

    if price_trend == "alta":
        # Prevendo um aumento baseado na tendência de alta
        next_price = latest_data['Close'] * (1 + np.random.uniform(0.001, 0.01))
    else:
        # Prevendo uma queda baseado na tendência de baixa
        next_price = latest_data['Close'] * (1 - np.random.uniform(0.001, 0.01))

    return next_price, price_trend

# Função para plotar o gráfico
def plot_chart(data):
    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'],
                                 name='Candlesticks'))

    # Médias Móveis
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA_9'], line=dict(color='blue', width=1), name='EMA 9'))
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], line=dict(color='orange', width=1), name='EMA 20'))
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA_50'], line=dict(color='red', width=1), name='EMA 50'))
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA_200'], line=dict(color='purple', width=1), name='EMA 200'))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_200'], line=dict(color='green', width=1), name='SMA 200'))
    fig.add_trace(go.Scatter(x=data.index, y=data['VWAP'], line=dict(color='black', width=1), name='VWAP'))

    # Layout
    fig.update_layout(title='Análise de BOVA11.SA',
                      xaxis_title='Data',
                      yaxis_title='Preço',
                      xaxis_rangeslider_visible=False)

    st.plotly_chart(fig)

# Função principal da aplicação
def main():
    st.title('Análise Gráfica de Ações da B3')

    ticker = st.text_input('Digite o ticker da ação', 'BOVA11.SA')

    if ticker:
        data = get_data(ticker)
        if data is not None and not data.empty:
            data = calculate_indicators(data)
            plot_chart(data)
            next_price, trend = predict_next_price(data)
            st.write(f"Tendência atual: {trend}")
            st.write(f"Preço sugerido para o próximo dia: R${next_price:.2f}")
        else:
            st.error('Dados não disponíveis para este ticker.')

if __name__ == "__main__":
    main()