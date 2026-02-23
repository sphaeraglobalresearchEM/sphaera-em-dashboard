"""
SPHAERA EMERGING MARKETS DASHBOARD
Simplified version with more countries
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="SPHAERA EM Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='font-size: 48px; color: #3B82F6;'>🌍 SPHAERA</h1>
        <p style='font-size: 20px; color: #60A5FA;'>EMERGING MARKETS INTELLIGENCE</p>
        <p style='font-size: 14px; color: #9CA3AF;'>Real-time tracking of frontier markets and capital flows</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"**Last Updated:** {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}")
st.markdown("---")

# ============================================================================
# DATA CONFIGURATION - EXPANDED LIST
# ============================================================================

EM_MARKETS = {
    # Latin America
    'Brazil': {'index': 'EWZ', 'currency': 'BRL=X', 'yield_10y': 12.5, 'policy_rate': 10.75, 'flag': '🇧🇷'},
    'Mexico': {'index': 'EWW', 'currency': 'MXN=X', 'yield_10y': 9.8, 'policy_rate': 10.25, 'flag': '🇲🇽'},
    'Argentina': {'index': 'ARGT', 'currency': 'ARS=X', 'yield_10y': 28.5, 'policy_rate': 40.00, 'flag': '🇦🇷'},
    'Chile': {'index': 'ECH', 'currency': 'CLP=X', 'yield_10y': 5.8, 'policy_rate': 5.75, 'flag': '🇨🇱'},
    'Colombia': {'index': 'GXG', 'currency': 'COP=X', 'yield_10y': 10.2, 'policy_rate': 10.75, 'flag': '🇨🇴'},
    
    # Asia
    'China': {'index': 'FXI', 'currency': 'CNY=X', 'yield_10y': 2.3, 'policy_rate': 3.10, 'flag': '🇨🇳'},
    'India': {'index': 'EPI', 'currency': 'INR=X', 'yield_10y': 7.1, 'policy_rate': 6.50, 'flag': '🇮🇳'},
    'Indonesia': {'index': 'EIDO', 'currency': 'IDR=X', 'yield_10y': 6.8, 'policy_rate': 6.00, 'flag': '🇮🇩'},
    'Thailand': {'index': 'THD', 'currency': 'THB=X', 'yield_10y': 2.8, 'policy_rate': 2.50, 'flag': '🇹🇭'},
    'Vietnam': {'index': 'VNM', 'currency': 'VND=X', 'yield_10y': 3.5, 'policy_rate': 4.50, 'flag': '🇻🇳'},
    'Philippines': {'index': 'EPHE', 'currency': 'PHP=X', 'yield_10y': 6.2, 'policy_rate': 6.00, 'flag': '🇵🇭'},
    'Malaysia': {'index': 'EWM', 'currency': 'MYR=X', 'yield_10y': 3.8, 'policy_rate': 3.00, 'flag': '🇲🇾'},
    
    # EMEA
    'South Africa': {'index': 'EZA', 'currency': 'ZAR=X', 'yield_10y': 10.2, 'policy_rate': 8.25, 'flag': '🇿🇦'},
    'Turkey': {'index': 'TUR', 'currency': 'TRY=X', 'yield_10y': 24.5, 'policy_rate': 50.00, 'flag': '🇹🇷'},
    'Poland': {'index': 'EPOL', 'currency': 'PLN=X', 'yield_10y': 5.9, 'policy_rate': 5.75, 'flag': '🇵🇱'},
    'UAE': {'index': 'UAE', 'currency': 'AED=X', 'yield_10y': 4.2, 'policy_rate': 5.40, 'flag': '🇦🇪'},
    'Saudi Arabia': {'index': 'KSA', 'currency': 'SAR=X', 'yield_10y': 4.8, 'policy_rate': 5.50, 'flag': '🇸🇦'},
    
    # Africa (Note: Some don't have ETFs, will show N/A for index)
    'Ghana': {'index': 'N/A', 'currency': 'GHS=X', 'yield_10y': 28.0, 'policy_rate': 29.00, 'flag': '🇬🇭'},
    'Zambia': {'index': 'N/A', 'currency': 'ZMW=X', 'yield_10y': 22.5, 'policy_rate': 13.50, 'flag': '🇿🇲'},
    'Morocco': {'index': 'N/A', 'currency': 'MAD=X', 'yield_10y': 3.5, 'policy_rate': 3.00, 'flag': '🇲🇦'},
    "Cote d'Ivoire": {'index': 'N/A', 'currency': 'XOF=X', 'yield_10y': 6.8, 'policy_rate': 3.50, 'flag': '🇨🇮'},
    'Nigeria': {'index': 'NGE', 'currency': 'NGN=X', 'yield_10y': 18.5, 'policy_rate': 27.25, 'flag': '🇳🇬'},
    'Egypt': {'index': 'EGPT', 'currency': 'EGP=X', 'yield_10y': 24.8, 'policy_rate': 27.25, 'flag': '🇪🇬'},
    'Kenya': {'index': 'N/A', 'currency': 'KES=X', 'yield_10y': 16.5, 'policy_rate': 12.75, 'flag': '🇰🇪'},
}

# ============================================================================
# SIMPLE DATA FETCH FUNCTION
# ============================================================================

@st.cache_data(ttl=300, show_spinner=False)
def get_price_change(ticker, days=30):
    """Get simple price change - returns 0 if fails"""
    try:
        if ticker == 'N/A':
            return 0.0
        
        data = yf.download(ticker, period=f'{days+10}d', progress=False)
        
        if data.empty or len(data) < 2:
            return 0.0
        
        current = float(data['Close'].iloc[-1])
        past = float(data['Close'].iloc[min(-days-1, -len(data))])
        
        change = ((current / past) - 1) * 100
        return round(change, 2)
    except:
        return 0.0

@st.cache_data(ttl=300, show_spinner=False)
def get_current_price(ticker):
    """Get current price"""
    try:
        if ticker == 'N/A':
            return 'N/A'
        
        data = yf.download(ticker, period='5d', progress=False)
        
        if data.empty:
            return 'N/A'
        
        return round(float(data['Close'].iloc[-1]), 2)
    except:
        return 'N/A'

@st.cache_data(ttl=300, show_spinner=False)
def get_ytd_performance(ticker):
    """Get Year-to-Date performance"""
    try:
        if ticker == 'N/A':
            return 0.0
        
        # Download data from Jan 1 of current year
        data = yf.download(ticker, period='1y', progress=False)
        
        if data.empty or len(data) < 2:
            return 0.0
        
        # Find first trading day of the year
        current_year = datetime.now().year
        year_start_data = data[data.index.year == current_year]
        
        if year_start_data.empty:
            return 0.0
        
        start_price = float(year_start_data['Close'].iloc[0])
        current_price = float(data['Close'].iloc[-1])
        
        ytd_change = ((current_price / start_price) - 1) * 100
        return round(ytd_change, 2)
    except:
        return 0.0

# ============================================================================
# BUILD DASHBOARD DATA
# ============================================================================

st.markdown("### 📊 Loading Market Data...")

progress_bar = st.progress(0)
status_text = st.empty()

dashboard_data = []
total = len(EM_MARKETS)

for idx, (country, info) in enumerate(EM_MARKETS.items()):
    status_text.text(f"Loading {country}... ({idx+1}/{total})")
    progress_bar.progress((idx + 1) / total)
    
    # Get data
    index_1m = get_price_change(info['index'], 30)
    index_3m = get_price_change(info['index'], 90)
    index_ytd = get_ytd_performance(info['index'])
    fx_1m = get_price_change(info['currency'], 30)
    current_price = get_current_price(info['index'])
    
    dashboard_data.append({
        'Flag': info['flag'],
        'Country': country,
        'Index': info['index'],
        'Price': current_price,
        '1M %': index_1m,
        '3M %': index_3m,
        'YTD %': index_ytd,
        'FX 1M %': fx_1m,
        '10Y Yield': info['yield_10y'],
        'Policy Rate': info['policy_rate'],
        'Term Premium': round(info['yield_10y'] - info['policy_rate'], 1)
    })
    
    time.sleep(0.1)  # Small delay to avoid rate limits

progress_bar.empty()
status_text.empty()

df = pd.DataFrame(dashboard_data)

st.success("✅ Data loaded successfully!")
st.markdown("---")

# ============================================================================
# KEY METRICS
# ============================================================================

st.markdown("### 📈 Market Snapshot")

col1, col2, col3, col4, col5 = st.columns(5)

# Filter out countries with valid data
valid_data = df[df['1M %'] != 0.0]
valid_ytd = df[df['YTD %'] != 0.0]

if not valid_data.empty:
    with col1:
        best = valid_data.loc[valid_data['1M %'].idxmax()]
        st.metric(
            "🏆 Best 1M",
            f"{best['Flag']} {best['Country']}",
            f"{best['1M %']:.1f}%"
        )
    
    with col2:
        worst = valid_data.loc[valid_data['1M %'].idxmin()]
        st.metric(
            "📉 Worst 1M",
            f"{worst['Flag']} {worst['Country']}",
            f"{worst['1M %']:.1f}%"
        )
    
    with col3:
        if not valid_ytd.empty:
            best_ytd = valid_ytd.loc[valid_ytd['YTD %'].idxmax()]
            st.metric(
                "🎯 Best YTD",
                f"{best_ytd['Flag']} {best_ytd['Country']}",
                f"{best_ytd['YTD %']:.1f}%"
            )
        else:
            st.metric("🎯 Best YTD", "Loading...", "0.0%")
    
    with col4:
        avg = valid_data['1M %'].mean()
        st.metric(
            "📊 Avg 1M",
            f"{avg:.1f}%",
            f"{len(valid_data[valid_data['1M %'] > 0])}/{len(valid_data)} +"
        )
    
    with col5:
        highest = df.loc[df['10Y Yield'].idxmax()]
        st.metric(
            "💰 High Yield",
            f"{highest['Flag']} {highest['Country']}",
            f"{highest['10Y Yield']:.1f}%"
        )

st.markdown("---")

# ============================================================================
# MAIN DATA TABLE
# ============================================================================

st.markdown("### 📋 Complete Market Overview")

# Color coding
def color_cells(val):
    if isinstance(val, (int, float)):
        if val > 0:
            return 'background-color: #1e3a1e; color: #90ee90'
        elif val < 0:
            return 'background-color: #3a1e1e; color: #ff9999'
    return ''

# Display options
display_cols = st.multiselect(
    "Select columns to display:",
    options=['Flag', 'Country', 'Index', 'Price', '1M %', '3M %', 'YTD %', 'FX 1M %', '10Y Yield', 'Policy Rate', 'Term Premium'],
    default=['Flag', 'Country', 'Index', '1M %', 'YTD %', 'FX 1M %', '10Y Yield', 'Policy Rate']
)

if display_cols:
    display_df = df[display_cols].copy()
    
    # Format numbers
    format_dict = {}
    if '1M %' in display_cols:
        format_dict['1M %'] = '{:.1f}%'
    if '3M %' in display_cols:
        format_dict['3M %'] = '{:.1f}%'
    if 'YTD %' in display_cols:
        format_dict['YTD %'] = '{:.1f}%'
    if 'FX 1M %' in display_cols:
        format_dict['FX 1M %'] = '{:.1f}%'
    if '10Y Yield' in display_cols:
        format_dict['10Y Yield'] = '{:.1f}%'
    if 'Policy Rate' in display_cols:
        format_dict['Policy Rate'] = '{:.2f}%'
    if 'Term Premium' in display_cols:
        format_dict['Term Premium'] = '{:.1f}pp'
    
    # Apply styling
    styled_df = display_df.style
    
    # Color performance columns
    perf_cols = [col for col in ['1M %', '3M %', 'YTD %', 'FX 1M %'] if col in display_cols]
    if perf_cols:
        styled_df = styled_df.applymap(color_cells, subset=perf_cols)
    
    if format_dict:
        styled_df = styled_df.format(format_dict)
    
    st.dataframe(styled_df, use_container_width=True, height=600)
else:
    st.warning("Please select at least one column to display")

# Download button
csv = df.to_csv(index=False)
st.download_button(
    "📥 Download Full Data (CSV)",
    csv,
    f"sphaera_em_{datetime.now().strftime('%Y%m%d')}.csv",
    "text/csv"
)

st.markdown("---")

# ============================================================================
# CHARTS
# ============================================================================

st.markdown("### 📊 Visual Analysis")

chart_type = st.radio(
    "Select chart type:",
    ["1-Month Performance", "YTD Performance", "FX Performance", "Yield Comparison", "Term Premium"],
    horizontal=True
)

if chart_type == "1-Month Performance":
    # Filter valid data
    chart_data = df[df['1M %'] != 0.0].sort_values('1M %')
    
    fig = px.bar(
        chart_data,
        y='Country',
        x='1M %',
        orientation='h',
        title='1-Month Index Performance (%)',
        color='1M %',
        color_continuous_scale=['red', 'yellow', 'green'],
        text='1M %'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "YTD Performance":
    # Filter valid data
    chart_data = df[df['YTD %'] != 0.0].sort_values('YTD %')
    
    fig = px.bar(
        chart_data,
        y='Country',
        x='YTD %',
        orientation='h',
        title=f'Year-to-Date Performance (Since Jan 1, {datetime.now().year}) (%)',
        color='YTD %',
        color_continuous_scale=['red', 'yellow', 'green'],
        text='YTD %'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "FX Performance":
    chart_data = df[df['FX 1M %'] != 0.0].sort_values('FX 1M %')
    
    fig = px.bar(
        chart_data,
        y='Country',
        x='FX 1M %',
        orientation='h',
        title='Currency Performance vs USD - 1 Month (%)',
        color='FX 1M %',
        color_continuous_scale=['red', 'yellow', 'green'],
        text='FX 1M %'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Yield Comparison":
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='10-Year Yield',
        x=df['Country'],
        y=df['10Y Yield'],
        marker_color='lightblue',
        text=df['10Y Yield'],
        texttemplate='%{text:.1f}%',
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name='Policy Rate',
        x=df['Country'],
        y=df['Policy Rate'],
        marker_color='lightgreen',
        text=df['Policy Rate'],
        texttemplate='%{text:.1f}%',
        textposition='outside'
    ))
    
    fig.update_layout(
        title='10-Year Yields vs Policy Rates',
        barmode='group',
        height=600,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Term Premium":
    chart_data = df.sort_values('Term Premium')
    
    fig = px.bar(
        chart_data,
        x='Country',
        y='Term Premium',
        title='Term Premium (10Y Yield - Policy Rate)',
        color='Term Premium',
        color_continuous_scale=['blue', 'yellow', 'red'],
        text='Term Premium'
    )
    fig.update_traces(texttemplate='%{text:.1f}pp', textposition='outside')
    fig.update_layout(height=600, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("## 🌍 SPHAERA Dashboard")
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Controls")
    
    if st.button("🔄 Refresh All Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📊 Coverage")
    st.markdown(f"""
    **Total Countries:** {len(EM_MARKETS)}
    
    **Regions:**
    - Latin America: 5
    - Asia: 7
    - EMEA: 6
    - Africa: 7
    
    **Data Points:**
    - Equity Indices
    - FX Rates (vs USD)
    - 10-Year Yields
    - Policy Rates
    - Term Premiums
    """)
    
    st.markdown("---")
    
    st.markdown("### 📝 Data Updates")
    st.markdown("""
    **Automatic (Real-time):**
    - Index prices
    - FX rates
    
    **Manual (Weekly):**
    - 10Y yields
    - Policy rates
    
    **Refresh:** Every 5 minutes
    """)
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    **SPHAERA Global Research**
    
    Emerging Markets Intelligence
    
    📧 sphaera.substack.com
    
    *Built with Streamlit + yfinance*
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
        <b>SPHAERA GLOBAL RESEARCH</b> | Emerging Markets Intelligence<br>
        Data: Yahoo Finance, Central Banks | Updated: Every 5 minutes<br>
        <i>For informational purposes only. Not investment advice.</i>
    </div>
""", unsafe_allow_html=True)
