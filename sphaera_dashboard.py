"""
SPHAERA EMERGING MARKETS DASHBOARD
Beautiful, Interactive EM Dashboard

SETUP:
1. Install: pip install streamlit yfinance pandas plotly --break-system-packages
2. Run: streamlit run sphaera_dashboard.py
3. Deploy: Push to GitHub, connect to streamlit.io (free)

"""

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="SPHAERA EM Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main container */
    .main {
        background-color: #0e1117;
    }
    
    /* Headers */
    h1 {
        color: #3B82F6;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    h2, h3 {
        color: #60A5FA;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 600;
    }
    
    /* Tables */
    .dataframe {
        font-size: 14px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1d29;
    }
    
    /* Cards */
    div[data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }
    
    /* Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1a1d29;
        color: #9CA3AF;
        text-align: center;
        padding: 10px;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA CONFIGURATION
# ============================================================================

EM_MARKETS = {
    'Brazil': {
        'index': 'EWZ',
        'currency': 'BRL=X',
        'yield_10y': 12.5,
        'policy_rate': 10.75,
        'flag': '🇧🇷'
    },
    'Mexico': {
        'index': 'EWW',
        'currency': 'MXN=X',
        'yield_10y': 9.8,
        'policy_rate': 10.25,
        'flag': '🇲🇽'
    },
    'South Africa': {
        'index': 'EZA',
        'currency': 'ZAR=X',
        'yield_10y': 10.2,
        'policy_rate': 8.25,
        'flag': '🇿🇦'
    },
    'Turkey': {
        'index': 'TUR',
        'currency': 'TRY=X',
        'yield_10y': 24.5,
        'policy_rate': 50.00,
        'flag': '🇹🇷'
    },
    'India': {
        'index': 'EPI',
        'currency': 'INR=X',
        'yield_10y': 7.1,
        'policy_rate': 6.50,
        'flag': '🇮🇳'
    },
    'China': {
        'index': 'FXI',
        'currency': 'CNY=X',
        'yield_10y': 2.3,
        'policy_rate': 3.10,
        'flag': '🇨🇳'
    },
    'Indonesia': {
        'index': 'EIDO',
        'currency': 'IDR=X',
        'yield_10y': 6.8,
        'policy_rate': 6.00,
        'flag': '🇮🇩'
    },
    'Poland': {
        'index': 'EPOL',
        'currency': 'PLN=X',
        'yield_10y': 5.9,
        'policy_rate': 5.75,
        'flag': '🇵🇱'
    },
    'Thailand': {
        'index': 'THD',
        'currency': 'THB=X',
        'yield_10y': 2.8,
        'policy_rate': 2.50,
        'flag': '🇹🇭'
    },
    'Argentina': {
        'index': 'ARGT',
        'currency': 'ARS=X',
        'yield_10y': 28.5,
        'policy_rate': 40.00,
        'flag': '🇦🇷'
    }
}

# ============================================================================
# HEADER
# ============================================================================

col1, col2, col3 = st.columns([2, 3, 2])

with col2:
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='font-size: 48px; margin-bottom: 0;'>🌍 SPHAERA</h1>
            <p style='font-size: 20px; color: #60A5FA; margin-top: 0;'>EMERGING MARKETS INTELLIGENCE</p>
            <p style='font-size: 14px; color: #9CA3AF;'>Real-time tracking of frontier markets, infrastructure investment, and capital flows</p>
        </div>
    """, unsafe_allow_html=True)

# Update timestamp
st.markdown(f"""
    <div style='text-align: center; color: #6B7280; font-size: 12px; margin-bottom: 30px;'>
        Last Updated: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}
    </div>
""", unsafe_allow_html=True)

# ============================================================================
# DATA FETCHING FUNCTIONS
# ============================================================================

@st.cache_data(ttl=300)
def fetch_data(ticker, period='3mo'):
    """Fetch historical data"""
    try:
        data = yf.download(ticker, period=period, progress=False)
        return data
    except:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def calculate_metrics(ticker, periods=[1, 7, 30, 90]):
    """Calculate returns and volatility"""
    data = fetch_data(ticker, period='6mo')
    
    if data.empty:
        return {f'{p}d': 0 for p in periods}
    
    metrics = {}
    current = data['Close'].iloc[-1]
    
    for period in periods:
        if len(data) > period:
            past = data['Close'].iloc[-period-1]
            ret = ((current / past) - 1) * 100
            metrics[f'{period}d'] = ret
    
    # Calculate volatility
    if len(data) > 30:
        returns = data['Close'].pct_change().dropna()
        metrics['volatility'] = returns.std() * np.sqrt(252) * 100
    else:
        metrics['volatility'] = 0
    
    return metrics

# ============================================================================
# BUILD DASHBOARD DATA
# ============================================================================

with st.spinner('Loading market data...'):
    dashboard_data = []
    
    for country, info in EM_MARKETS.items():
        index_metrics = calculate_metrics(info['index'])
        fx_metrics = calculate_metrics(info['currency'])
        
        dashboard_data.append({
            'Flag': info['flag'],
            'Country': country,
            'Index': info['index'],
            '1D %': index_metrics.get('1d', 0),
            '1W %': index_metrics.get('7d', 0),
            '1M %': index_metrics.get('30d', 0),
            '3M %': index_metrics.get('90d', 0),
            'Vol': index_metrics.get('volatility', 0),
            'FX 1M %': fx_metrics.get('30d', 0),
            '10Y Yield': info['yield_10y'],
            'Policy Rate': info['policy_rate'],
            'Term Premium': info['yield_10y'] - info['policy_rate']
        })
    
    df = pd.DataFrame(dashboard_data)

# ============================================================================
# KEY METRICS ROW
# ============================================================================

st.markdown("### 📊 Market Snapshot")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    best = df.loc[df['1M %'].idxmax()]
    st.metric(
        label="🏆 Best Performer (1M)",
        value=f"{best['Flag']} {best['Country']}",
        delta=f"{best['1M %']:.2f}%",
        delta_color="normal"
    )

with col2:
    worst = df.loc[df['1M %'].idxmin()]
    st.metric(
        label="📉 Worst Performer (1M)",
        value=f"{worst['Flag']} {worst['Country']}",
        delta=f"{worst['1M %']:.2f}%",
        delta_color="inverse"
    )

with col3:
    avg = df['1M %'].mean()
    st.metric(
        label="📈 EM Average Return",
        value=f"{avg:.2f}%",
        delta=f"{len(df[df['1M %'] > 0])} / {len(df)} positive"
    )

with col4:
    highest_yield = df.loc[df['10Y Yield'].idxmax()]
    st.metric(
        label="💰 Highest Yield",
        value=f"{highest_yield['Flag']} {highest_yield['Country']}",
        delta=f"{highest_yield['10Y Yield']:.1f}%"
    )

with col5:
    best_fx = df.loc[df['FX 1M %'].idxmax()]
    st.metric(
        label="💱 Strongest Currency",
        value=f"{best_fx['Flag']} {best_fx['Country']}",
        delta=f"{best_fx['FX 1M %']:.2f}%"
    )

st.markdown("---")

# ============================================================================
# MAIN DATA TABLE
# ============================================================================

st.markdown("### 📋 Market Overview")

# Format and display
display_df = df.copy()

# Color coding function
def highlight_performance(val):
    if isinstance(val, (int, float)):
        if val > 2:
            return 'background-color: #064e3b; color: #6ee7b7'
        elif val > 0:
            return 'background-color: #14532d; color: #86efac'
        elif val < -2:
            return 'background-color: #7f1d1d; color: #fca5a5'
        elif val < 0:
            return 'background-color: #991b1b; color: #fecaca'
    return ''

styled_df = display_df.style\
    .applymap(highlight_performance, subset=['1D %', '1W %', '1M %', '3M %', 'FX 1M %'])\
    .format({
        '1D %': '{:.2f}%',
        '1W %': '{:.2f}%',
        '1M %': '{:.2f}%',
        '3M %': '{:.2f}%',
        'FX 1M %': '{:.2f}%',
        'Vol': '{:.1f}%',
        '10Y Yield': '{:.1f}%',
        'Policy Rate': '{:.2f}%',
        'Term Premium': '{:.1f}pp'
    })\
    .background_gradient(subset=['10Y Yield'], cmap='RdYlGn_r')\
    .background_gradient(subset=['Vol'], cmap='YlOrRd')

st.dataframe(styled_df, use_container_width=True, height=450)

st.markdown("---")

# ============================================================================
# INTERACTIVE CHARTS
# ============================================================================

st.markdown("### 📊 Performance Analysis")

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📈 Returns", "💱 FX Performance", "📉 Yields", "🎯 Risk-Return"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # 1M Performance
        fig_1m = px.bar(
            df.sort_values('1M %', ascending=True),
            y='Country',
            x='1M %',
            orientation='h',
            title='1-Month Index Performance',
            color='1M %',
            color_continuous_scale=['#dc2626', '#facc15', '#22c55e'],
            text='1M %',
            labels={'1M %': '1-Month Return (%)'}
        )
        fig_1m.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_1m.update_layout(
            height=500,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E5E7EB')
        )
        st.plotly_chart(fig_1m, use_container_width=True)
    
    with col2:
        # 3M Performance
        fig_3m = px.bar(
            df.sort_values('3M %', ascending=True),
            y='Country',
            x='3M %',
            orientation='h',
            title='3-Month Index Performance',
            color='3M %',
            color_continuous_scale=['#dc2626', '#facc15', '#22c55e'],
            text='3M %',
            labels={'3M %': '3-Month Return (%)'}
        )
        fig_3m.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_3m.update_layout(
            height=500,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E5E7EB')
        )
        st.plotly_chart(fig_3m, use_container_width=True)

with tab2:
    # FX Performance
    fig_fx = px.bar(
        df.sort_values('FX 1M %', ascending=True),
        y='Country',
        x='FX 1M %',
        orientation='h',
        title='Currency Performance vs USD (1 Month)',
        color='FX 1M %',
        color_continuous_scale=['#dc2626', '#facc15', '#22c55e'],
        text='FX 1M %',
        labels={'FX 1M %': 'FX Return vs USD (%)'}
    )
    fig_fx.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_fx.update_layout(
        height=600,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E5E7EB')
    )
    st.plotly_chart(fig_fx, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # Yields comparison
        fig_yields = go.Figure()
        fig_yields.add_trace(go.Bar(
            name='10Y Yield',
            x=df['Country'],
            y=df['10Y Yield'],
            marker_color='#3B82F6',
            text=df['10Y Yield'],
            texttemplate='%{text:.1f}%',
            textposition='outside'
        ))
        fig_yields.add_trace(go.Bar(
            name='Policy Rate',
            x=df['Country'],
            y=df['Policy Rate'],
            marker_color='#10B981',
            text=df['Policy Rate'],
            texttemplate='%{text:.1f}%',
            textposition='outside'
        ))
        fig_yields.update_layout(
            title='10-Year Yields vs Policy Rates',
            barmode='group',
            yaxis_title='Rate (%)',
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E5E7EB')
        )
        st.plotly_chart(fig_yields, use_container_width=True)
    
    with col2:
        # Term premium
        fig_term = px.bar(
            df.sort_values('Term Premium'),
            x='Country',
            y='Term Premium',
            title='Term Premium (10Y Yield - Policy Rate)',
            color='Term Premium',
            color_continuous_scale=['#3B82F6', '#10B981', '#F59E0B', '#EF4444'],
            text='Term Premium',
            labels={'Term Premium': 'Term Premium (pp)'}
        )
        fig_term.update_traces(texttemplate='%{text:.1f}pp', textposition='outside')
        fig_term.update_layout(
            height=500,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E5E7EB')
        )
        st.plotly_chart(fig_term, use_container_width=True)

with tab4:
    # Risk-Return scatter
    fig_scatter = px.scatter(
        df,
        x='Vol',
        y='1M %',
        size='10Y Yield',
        color='3M %',
        text='Country',
        title='Risk-Return Profile (Volatility vs 1M Return)',
        labels={'Vol': 'Volatility (annualized %)', '1M %': '1-Month Return (%)'},
        color_continuous_scale=['#dc2626', '#facc15', '#22c55e'],
        size_max=30
    )
    fig_scatter.update_traces(textposition='top center', textfont_size=10)
    fig_scatter.update_layout(
        height=600,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E5E7EB')
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# ============================================================================
# HISTORICAL PRICE CHARTS
# ============================================================================

st.markdown("### 📉 Historical Performance")

# Country selector
selected_countries = st.multiselect(
    'Select countries to compare (max 5):',
    options=list(EM_MARKETS.keys()),
    default=['Brazil', 'Mexico', 'South Africa'],
    max_selections=5
)

# Period selector
period_option = st.selectbox(
    'Time Period:',
    options=['1 Month', '3 Months', '6 Months', '1 Year'],
    index=2
)

period_map = {
    '1 Month': '1mo',
    '3 Months': '3mo',
    '6 Months': '6mo',
    '1 Year': '1y'
}

if selected_countries:
    fig_history = go.Figure()
    
    for country in selected_countries:
        ticker = EM_MARKETS[country]['index']
        data = fetch_data(ticker, period=period_map[period_option])
        
        if not data.empty:
            # Normalize to 100
            normalized = (data['Close'] / data['Close'].iloc[0]) * 100
            
            fig_history.add_trace(go.Scatter(
                x=data.index,
                y=normalized,
                mode='lines',
                name=f"{EM_MARKETS[country]['flag']} {country}",
                line=dict(width=3),
                hovertemplate='<b>%{fullData.name}</b><br>Date: %{x}<br>Value: %{y:.2f}<extra></extra>'
            ))
    
    fig_history.update_layout(
        title=f'Normalized Index Performance (Base = 100) - {period_option}',
        xaxis_title='Date',
        yaxis_title='Indexed Value',
        height=500,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E5E7EB'),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    st.plotly_chart(fig_history, use_container_width=True)
else:
    st.info("👆 Select countries above to view historical performance")

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("## ⚙️ Dashboard Controls")
    
    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    
    # Export
    st.markdown("## 💾 Export Data")
    
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"sphaera_em_dashboard_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Data sources
    st.markdown("## 📊 Data Sources")
    st.markdown("""
    **Real-time:**
    - Index prices (Yahoo Finance)
    - FX rates (Yahoo Finance)
    
    **Weekly updates:**
    - 10Y yields (Investing.com)
    - Policy rates (Central Banks)
    
    **Update frequency:** Every 5 minutes
    """)
    
    st.markdown("---")
    
    # Filters
    st.markdown("## 🔍 Filters")
    
    min_yield = st.slider(
        "Minimum 10Y Yield (%)",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=0.5
    )
    
    if min_yield > 0:
        filtered = df[df['10Y Yield'] >= min_yield]
        st.info(f"**{len(filtered)}** countries with yield ≥ {min_yield}%")
    
    st.markdown("---")
    
    # About
    st.markdown("## ℹ️ About")
    st.markdown("""
    **SPHAERA Global Research**
    
    Emerging Markets Intelligence
    
    Real-time tracking of:
    - 10 major EM economies
    - Equity indices
    - Currency movements
    - Bond yields
    - Policy rates
    
    Built with Streamlit + yfinance
    
    ---
    
    📧 sphaera.substack.com
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6B7280; font-size: 12px; padding: 20px;'>
        <b>SPHAERA GLOBAL RESEARCH</b> | Emerging Markets Intelligence<br>
        Data sources: Yahoo Finance, Central Banks, Investing.com<br>
        <i>This dashboard is for informational purposes only. Not investment advice. Conduct your own due diligence.</i>
    </div>
""", unsafe_allow_html=True)
