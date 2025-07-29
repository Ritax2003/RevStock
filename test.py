import streamlit as st
import pandas as pd
import plotly.graph_objects as go



# ----- Page Config -----
st.set_page_config(layout="wide", page_title="RevStock")

# ----- Load Data -----
df = pd.read_csv("All.csv")
df.columns = df.columns.str.strip()
df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
df.sort_values("Date", inplace=True)

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month_name()

# ----- Header KPIs -----
st.title("RevStock")
st.markdown("""
    <style>
    .kpi-card {
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-family: sans-serif;
    }
    .kpi-title {
        font-size: 16px;
        color: #555;
    }
    .kpi-value {
        font-size: 22px;
        font-weight: bold;
        color: #222;
    }
    .kpi-green {
        color: green;
    }
    .kpi-red{
            color:red;
    }
    </style>
""", unsafe_allow_html=True)

# Symbol Selector
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Ticker</div>
    """, unsafe_allow_html=True)
    selected_symbol = st.selectbox(
        "",
        sorted(df["symbol"].unique()),
        key="ticker_select"
        
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
# Filter the DataFrame by selected symbol (before year/month filters)
df = df[df["symbol"] == selected_symbol]

# ----- Sidebar Filters -----
st.sidebar.title("Filter")
years = st.sidebar.multiselect("Year", sorted(df["Year"].unique()), default=df["Year"].max())
months = st.sidebar.multiselect("Month", df["Month"].unique(), default=list(df["Month"].unique()))

filtered_df = df[df["Year"].isin(years) & df["Month"].isin(months)]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

latest_row = filtered_df.iloc[-1]

with col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Open</div>
            <div class="kpi-value">${latest_row['open']:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">High</div>
            <div class="kpi-value kpi-green">${latest_row['high']:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Low</div>
            <div class="kpi-value kpi-red">${latest_row['low']:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Close</div>
            <div class="kpi-value">${latest_row['close']:.2f}</div>
        </div>
    """, unsafe_allow_html=True)


st.markdown("---")

# ----- Graph Layout: 2 Columns -----
left_col, right_col = st.columns([1, 1.2])

# Left Column: Scatter + Volume
with left_col:
    st.subheader("High vs Low Comparison with Volume")
    scatter_fig = go.Figure(
        go.Scatter(
            x=filtered_df["high"],
            y=filtered_df["low"],
            mode="markers",
            marker=dict(
                size=filtered_df["change"].abs() * 5,
                color=filtered_df["close"],
                colorscale="Viridis",
                showscale=True
            ),
            text=filtered_df["Date"].dt.strftime('%Y-%m-%d')
        )
    )
    scatter_fig.update_layout(
        xaxis_title="High",
        yaxis_title="Low",
        height=300,
        margin=dict(t=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
        title_font=dict(size=16, family="Arial", color="black", weight="bold"),
        tickfont=dict(size=14, family="Arial", color="black"),
        ),
        yaxis=dict(
        title_font=dict(size=16, family="Arial", color="black", weight="bold"),
        tickfont=dict(size=14, family="Arial", color="black"),
        ),
    )
    st.plotly_chart(scatter_fig, use_container_width=True)

    st.subheader("Historical Volume")
    volume_fig = go.Figure()
    volume_fig.add_trace(go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["volume"]/1000000,
        mode="lines+markers",
        name="Volume"
    ))
    volume_fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Volume",
        height=250,
        margin=dict(t=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
        title_font=dict(size=16, family="Arial", color="black", weight="bold"),
        tickfont=dict(size=14, family="Arial", color="black"),
        ),
        yaxis=dict(
        title_font=dict(size=16, family="Arial", color="black", weight="bold"),
        tickfont=dict(size=14, family="Arial", color="black"),
        ),
    )
    st.plotly_chart(volume_fig, use_container_width=True)

# Right Column: Candlestick
with right_col:
    st.subheader("Candlestick Chart")
    candlestick_fig = go.Figure(data=[go.Candlestick(
        x=filtered_df["Date"],
        open=filtered_df["open"],
        high=filtered_df["high"],
        low=filtered_df["low"],
        close=filtered_df["close"]
    )])
    candlestick_fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        height=600,
        margin=dict(t=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title_font=dict(size=16, family="Arial", color="black", weight="bold"),
            tickfont=dict(size=14, family="Arial", color="black"),
            rangeslider=dict(visible=False) # TO REMOVE THE RANGE SLIDER
        ),
        yaxis=dict(
        tickfont=dict(size=14, family="Arial", color="black"),
        title_font=dict(size=16, family="Arial", color="black", weight="bold")
        ),
    )
    st.plotly_chart(candlestick_fig, use_container_width=True)
