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

# ============================================================================
# DATA CONFIGURATION - EXPANDED LIST
# ============================================================================

# Store previous month's yields for change tracking
# Update these manually each month when you update current yields
PREVIOUS_YIELDS = {
    'Brazil': 12.3, 'Mexico': 9.9, 'Argentina': 27.8, 'Chile': 5.9, 'Colombia': 10.0,
    'China': 2.2, 'India': 7.0, 'Indonesia': 6.9, 'Thailand': 2.7, 'Vietnam': 3.4,
    'Philippines': 6.3, 'Malaysia': 3.9, 'Taiwan': 1.4, 'Japan': 1.1,
    'South Africa': 10.0, 'Turkey': 25.2, 'Poland': 6.0, 'UAE': 4.1, 'Saudi Arabia': 4.7,
    'Ghana': 27.5, 'Zambia': 22.0, 'Morocco': 3.4, "Cote d'Ivoire": 6.7,
    'Nigeria': 18.0, 'Egypt': 24.5, 'Kenya': 16.2
}

EM_MARKETS = {
    # Latin America
    'Brazil': {'index': 'EWZ', 'currency': 'BRL=X', 'yield_10y': 12.5, 'policy_rate': 10.75, 'inflation': 4.5, 'flag': '🇧🇷'},
    'Mexico': {'index': 'EWW', 'currency': 'MXN=X', 'yield_10y': 9.8, 'policy_rate': 10.25, 'inflation': 4.3, 'flag': '🇲🇽'},
    'Argentina': {'index': 'ARGT', 'currency': 'ARS=X', 'yield_10y': 28.5, 'policy_rate': 40.00, 'inflation': 211.4, 'flag': '🇦🇷'},
    'Chile': {'index': 'ECH', 'currency': 'CLP=X', 'yield_10y': 5.8, 'policy_rate': 5.75, 'inflation': 4.2, 'flag': '🇨🇱'},
    'Colombia': {'index': 'GXG', 'currency': 'COP=X', 'yield_10y': 10.2, 'policy_rate': 10.75, 'inflation': 5.8, 'flag': '🇨🇴'},
    
    # Asia
    'China': {'index': 'FXI', 'currency': 'CNY=X', 'yield_10y': 2.3, 'policy_rate': 3.10, 'inflation': 0.7, 'flag': '🇨🇳'},
    'India': {'index': 'EPI', 'currency': 'INR=X', 'yield_10y': 7.1, 'policy_rate': 6.50, 'inflation': 5.2, 'flag': '🇮🇳'},
    'Indonesia': {'index': 'EIDO', 'currency': 'IDR=X', 'yield_10y': 6.8, 'policy_rate': 6.00, 'inflation': 1.8, 'flag': '🇮🇩'},
    'Thailand': {'index': 'THD', 'currency': 'THB=X', 'yield_10y': 2.8, 'policy_rate': 2.50, 'inflation': 0.4, 'flag': '🇹🇭'},
    'Vietnam': {'index': 'VNM', 'currency': 'VND=X', 'yield_10y': 3.5, 'policy_rate': 4.50, 'inflation': 3.8, 'flag': '🇻🇳'},
    'Philippines': {'index': 'EPHE', 'currency': 'PHP=X', 'yield_10y': 6.2, 'policy_rate': 6.00, 'inflation': 2.9, 'flag': '🇵🇭'},
    'Malaysia': {'index': 'EWM', 'currency': 'MYR=X', 'yield_10y': 3.8, 'policy_rate': 3.00, 'inflation': 1.5, 'flag': '🇲🇾'},
    'Taiwan': {'index': 'EWT', 'currency': 'TWD=X', 'yield_10y': 1.5, 'policy_rate': 2.00, 'inflation': 2.3, 'flag': '🇹🇼'},
    'Japan': {'index': 'EWJ', 'currency': 'JPY=X', 'yield_10y': 1.2, 'policy_rate': 0.25, 'inflation': 2.8, 'flag': '🇯🇵'},
    
    # EMEA
    'South Africa': {'index': 'EZA', 'currency': 'ZAR=X', 'yield_10y': 10.2, 'policy_rate': 8.25, 'inflation': 5.3, 'flag': '🇿🇦'},
    'Turkey': {'index': 'TUR', 'currency': 'TRY=X', 'yield_10y': 24.5, 'policy_rate': 50.00, 'inflation': 64.8, 'flag': '🇹🇷'},
    'Poland': {'index': 'EPOL', 'currency': 'PLN=X', 'yield_10y': 5.9, 'policy_rate': 5.75, 'inflation': 4.7, 'flag': '🇵🇱'},
    'UAE': {'index': 'UAE', 'currency': 'AED=X', 'yield_10y': 4.2, 'policy_rate': 5.40, 'inflation': 3.5, 'flag': '🇦🇪'},
    'Saudi Arabia': {'index': 'KSA', 'currency': 'SAR=X', 'yield_10y': 4.8, 'policy_rate': 5.50, 'inflation': 1.6, 'flag': '🇸🇦'},
    
    # Africa (Note: Some don't have ETFs, will show N/A for index)
    'Ghana': {'index': 'N/A', 'currency': 'GHS=X', 'yield_10y': 28.0, 'policy_rate': 29.00, 'inflation': 23.2, 'flag': '🇬🇭'},
    'Zambia': {'index': 'N/A', 'currency': 'ZMW=X', 'yield_10y': 22.5, 'policy_rate': 13.50, 'inflation': 13.8, 'flag': '🇿🇲'},
    'Morocco': {'index': 'N/A', 'currency': 'MAD=X', 'yield_10y': 3.5, 'policy_rate': 3.00, 'inflation': 1.9, 'flag': '🇲🇦'},
    "Cote d'Ivoire": {'index': 'N/A', 'currency': 'XOF=X', 'yield_10y': 6.8, 'policy_rate': 3.50, 'inflation': 4.1, 'flag': '🇨🇮'},
    'Nigeria': {'index': 'NGE', 'currency': 'NGN=X', 'yield_10y': 18.5, 'policy_rate': 27.25, 'inflation': 34.6, 'flag': '🇳🇬'},
    'Egypt': {'index': 'EGPT', 'currency': 'EGP=X', 'yield_10y': 24.8, 'policy_rate': 27.25, 'inflation': 25.5, 'flag': '🇪🇬'},
    'Kenya': {'index': 'N/A', 'currency': 'KES=X', 'yield_10y': 16.5, 'policy_rate': 12.75, 'inflation': 2.8, 'flag': '🇰🇪'},
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
    
    # Calculate yield change (current - previous)
    current_yield = info['yield_10y']
    previous_yield = PREVIOUS_YIELDS.get(country, current_yield)
    yield_change = current_yield - previous_yield
    
    # Calculate Real Rate (Policy Rate - Inflation)
    real_rate = info['policy_rate'] - info['inflation']
    
    dashboard_data.append({
        'Flag': info['flag'],
        'Country': country,
        'Index': info['index'],
        'Price': current_price,
        '1M %': index_1m,
        '3M %': index_3m,
        'YTD %': index_ytd,
        'FX 1M %': fx_1m,
        '10Y Yield': current_yield,
        'Yield Δ': yield_change,
        'Inflation': info['inflation'],
        'Real Rate': real_rate,
        'Policy Rate': info['policy_rate'],
        'Term Premium': round(current_yield - info['policy_rate'], 1)
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

def color_yield_change(val):
    """Color yield changes: RED for rising (bad for bonds), GREEN for falling (good for bonds)"""
    if isinstance(val, (int, float)):
        if val > 0.1:  # Yields rising
            return 'background-color: #3a1e1e; color: #ff9999; font-weight: bold'
        elif val < -0.1:  # Yields falling
            return 'background-color: #1e3a1e; color: #90ee90; font-weight: bold'
    return ''

def color_real_rate(val):
    """Color real rates: RED for negative (loose policy), GREEN for positive/restrictive"""
    if isinstance(val, (int, float)):
        if val < -5:  # Very negative (extremely loose)
            return 'background-color: #4a1e1e; color: #ff6666; font-weight: bold'
        elif val < 0:  # Negative (loose policy)
            return 'background-color: #3a1e1e; color: #ff9999'
        elif val > 3:  # Very positive (very restrictive)
            return 'background-color: #1e4a1e; color: #66ff66; font-weight: bold'
        elif val > 0:  # Positive (restrictive)
            return 'background-color: #1e3a1e; color: #90ee90'
    return ''

# Display options
display_cols = st.multiselect(
    "Select columns to display:",
    options=['Flag', 'Country', 'Index', 'Price', '1M %', '3M %', 'YTD %', 'FX 1M %', '10Y Yield', 'Yield Δ', 'Inflation', 'Real Rate', 'Policy Rate', 'Term Premium'],
    default=['Flag', 'Country', 'Index', '1M %', 'YTD %', 'FX 1M %', '10Y Yield', 'Yield Δ', 'Inflation', 'Real Rate', 'Policy Rate']
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
    if 'Yield Δ' in display_cols:
        format_dict['Yield Δ'] = '{:+.1f}bp'  # Show + or - sign
    if 'Inflation' in display_cols:
        format_dict['Inflation'] = '{:.1f}%'
    if 'Real Rate' in display_cols:
        format_dict['Real Rate'] = '{:+.1f}%'  # Show + or - sign
    if 'Policy Rate' in display_cols:
        format_dict['Policy Rate'] = '{:.2f}%'
    if 'Term Premium' in display_cols:
        format_dict['Term Premium'] = '{:.1f}pp'
    
    # Apply styling
    styled_df = display_df.style
    
    # Color performance columns (green = good, red = bad)
    perf_cols = [col for col in ['1M %', '3M %', 'YTD %', 'FX 1M %'] if col in display_cols]
    if perf_cols:
        styled_df = styled_df.applymap(color_cells, subset=perf_cols)
    
    # Color yield changes (RED = rising, GREEN = falling)
    if 'Yield Δ' in display_cols:
        styled_df = styled_df.applymap(color_yield_change, subset=['Yield Δ'])
    
    # Color real rates (RED = negative/loose, GREEN = positive/tight)
    if 'Real Rate' in display_cols:
        styled_df = styled_df.applymap(color_real_rate, subset=['Real Rate'])
    
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
    ["1-Month Performance", "YTD Performance", "FX Performance", "Yield Comparison", "Yield Changes", "Real Rates", "Term Premium"],
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

elif chart_type == "Yield Changes":
    # Sort by yield change magnitude
    chart_data = df.sort_values('Yield Δ')
    
    # Create colors: red for positive (rising yields), green for negative (falling)
    colors = ['#ff4444' if x > 0 else '#44ff44' if x < 0 else '#888888' 
              for x in chart_data['Yield Δ']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=chart_data['Yield Δ'],
        y=chart_data['Country'],
        orientation='h',
        marker_color=colors,
        text=chart_data['Yield Δ'],
        texttemplate='%{text:+.1f}bp',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Yield Change: %{x:+.1f}bp<br>' +
                      'Direction: ' + chart_data['Direction'].astype(str) + '<extra></extra>'
    ))
    
    fig.update_layout(
        title='10-Year Yield Changes (1 Month)<br><sub>🔴 RED = Rising Yields (Bad for Bonds) | 🟢 GREEN = Falling Yields (Good for Bonds)</sub>',
        xaxis_title='Basis Points Change',
        yaxis_title='',
        height=600,
        showlegend=False,
        # Add vertical line at zero
        shapes=[dict(
            type='line',
            x0=0, x1=0,
            y0=-0.5, y1=len(chart_data)-0.5,
            line=dict(color='white', width=2, dash='dash')
        )]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add explanation
    st.info("""
    **How to read this chart:**
    - 🔴 **RED bars (right)** = Yields RISING = Bond prices falling = Tightening conditions
    - 🟢 **GREEN bars (left)** = Yields FALLING = Bond prices rising = Easing conditions
    - **Larger bars** = Bigger moves in yields over the past month
    """)

elif chart_type == "Real Rates":
    # Sort by real rate
    chart_data = df.sort_values('Real Rate')
    
    # Create colors: green for positive (tight policy), red for negative (loose policy)
    colors = ['#44ff44' if x > 3 else '#90ee90' if x > 0 else '#ff9999' if x > -5 else '#ff4444' 
              for x in chart_data['Real Rate']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=chart_data['Real Rate'],
        y=chart_data['Country'],
        orientation='h',
        marker_color=colors,
        text=chart_data['Real Rate'],
        texttemplate='%{text:+.1f}%',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>' +
                      'Real Rate: %{x:+.1f}%<br>' +
                      'Policy Rate: ' + chart_data['Policy Rate'].astype(str) + '%<br>' +
                      'Inflation: ' + chart_data['Inflation'].astype(str) + '%<extra></extra>'
    ))
    
    fig.update_layout(
        title='Real Policy Rates (Policy Rate - Inflation)<br><sub>🟢 GREEN = Restrictive (Positive) | 🔴 RED = Accommodative (Negative)</sub>',
        xaxis_title='Real Rate (%)',
        yaxis_title='',
        height=600,
        showlegend=False,
        # Add vertical line at zero
        shapes=[dict(
            type='line',
            x0=0, x1=0,
            y0=-0.5, y1=len(chart_data)-0.5,
            line=dict(color='white', width=2, dash='dash')
        )]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add explanation
    st.info("""
    **How to read this chart:**
    - 🟢 **GREEN bars (right)** = POSITIVE real rates = Restrictive policy = Fighting inflation
    - 🔴 **RED bars (left)** = NEGATIVE real rates = Accommodative policy = Inflation exceeding rates
    - **Zero line** = Neutral policy (policy rate equals inflation)
    
    **Examples:**
    - Turkey at -14%: Policy rate (50%) - Inflation (64%) = Extremely loose despite high rates
    - Brazil at +6%: Policy rate (10.75%) - Inflation (4.5%) = Very restrictive, suppressing growth
    """)

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
    - Asia: 9 (incl. Taiwan & Japan)
    - EMEA: 5
    - Africa: 7
    
    **Data Points:**
    - Equity Indices
    - FX Rates (vs USD)
    - 10-Year Yields
    - Yield Changes (1M)
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
