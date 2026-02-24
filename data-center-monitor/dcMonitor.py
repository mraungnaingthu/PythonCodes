import streamlit as st
import psutil
import time
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import threading

# Page configuration
st.set_page_config(
    page_title="Data Center Monitor",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for data center theme
st.markdown("""
<style>
    .stApp {
        background-color: #0a1929;
        color: white;
    }

    .server-card {
        background: linear-gradient(135deg, #1a365d 0%, #0a1929 100%);
        border-radius: 10px;
        padding: 20px;
        border-left: 4px solid #00cc88;
        margin-bottom: 10px;
    }

    .server-card-warning {
        border-left-color: #ffc107 !important;
    }

    .server-card-down {
        border-left-color: #ff4757 !important;
    }

    .metric-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }

    .live-badge {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)


# Simulated data center servers
def get_servers():
    return [
        {"id": 1, "name": "WEB-01", "ip": "192.168.1.10", "type": "Web Server", "status": "up", "cpu": 45,
         "memory": 68},
        {"id": 2, "name": "DB-01", "ip": "192.168.1.20", "type": "Database", "status": "up", "cpu": 23, "memory": 45},
        {"id": 3, "name": "CACHE-01", "ip": "192.168.1.30", "type": "Redis Cache", "status": "warning", "cpu": 82,
         "memory": 78},
        {"id": 4, "name": "LB-01", "ip": "192.168.1.40", "type": "Load Balancer", "status": "down", "cpu": 0,
         "memory": 0},
        {"id": 5, "name": "BACKUP-01", "ip": "192.168.1.50", "type": "Backup Server", "status": "up", "cpu": 12,
         "memory": 34},
        {"id": 6, "name": "MONITOR-01", "ip": "192.168.1.60", "type": "Monitoring", "status": "up", "cpu": 8,
         "memory": 22},
    ]


# Get real system metrics
def get_system_metrics():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "network_sent": psutil.net_io_counters().bytes_sent,
        "network_recv": psutil.net_io_counters().bytes_recv,
        "temperature": random.randint(30, 50)  # Simulated temperature
    }


# Create gauge chart
def create_gauge(value, title, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'color': 'white'}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': "white"},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': 'rgba(0, 204, 136, 0.2)'},
                {'range': [50, 80], 'color': 'rgba(255, 193, 7, 0.2)'},
                {'range': [80, 100], 'color': 'rgba(255, 71, 87, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"},
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


# Main dashboard
def main():
    # Title with live indicator
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🖥️ Data Center Monitoring Dashboard")
        st.markdown("*Real-time infrastructure monitoring for data center operations*")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<span class="live-badge" style="color:#00cc88">● LIVE</span>', unsafe_allow_html=True)

    # Get metrics
    metrics = get_system_metrics()
    servers = get_servers()

    # KPI Metrics Row
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("CPU Usage", f"{metrics['cpu']:.1f}%", delta="2%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("Memory", f"{metrics['memory']:.1f}%", delta="-1%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("Disk", f"{metrics['disk']:.1f}%", delta="0.5%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("Temperature", f"{metrics['temperature']}°C", delta="+1°C")
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        active_servers = len([s for s in servers if s['status'] == 'up'])
        st.metric("Active Servers", f"{active_servers}/{len(servers)}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Two columns for charts and server list
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # System gauges
        st.subheader("System Health")
        gauge_col1, gauge_col2, gauge_col3 = st.columns(3)

        with gauge_col1:
            st.plotly_chart(create_gauge(metrics['cpu'], "CPU", "#0066cc"), use_container_width=True)

        with gauge_col2:
            st.plotly_chart(create_gauge(metrics['memory'], "Memory", "#00cc88"), use_container_width=True)

        with gauge_col3:
            st.plotly_chart(create_gauge(metrics['disk'], "Disk", "#9c88ff"), use_container_width=True)

        # Network traffic chart
        st.subheader("Network Traffic")
        network_data = pd.DataFrame({
            'Time': [datetime.now() - timedelta(minutes=i) for i in range(30, 0, -1)],
            'Upload (MB)': [random.randint(10, 100) for _ in range(30)],
            'Download (MB)': [random.randint(20, 150) for _ in range(30)]
        })

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=network_data['Time'],
            y=network_data['Upload (MB)'],
            name='Upload',
            line=dict(color='#0066cc', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 102, 204, 0.1)'
        ))
        fig.add_trace(go.Scatter(
            x=network_data['Time'],
            y=network_data['Download (MB)'],
            name='Download',
            line=dict(color='#00cc88', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 204, 136, 0.1)'
        ))

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white"},
            height=300,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Server status
        st.subheader("Server Status")

        for server in servers:
            status_color = {
                'up': '#00cc88',
                'warning': '#ffc107',
                'down': '#ff4757'
            }

            status_icon = {
                'up': '✅',
                'warning': '⚠️',
                'down': '❌'
            }

            card_class = "server-card"
            if server['status'] == 'warning':
                card_class += " server-card-warning"
            elif server['status'] == 'down':
                card_class += " server-card-down"

            st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{server['name']}</strong><br>
                        <small style="color: #aaa;">{server['ip']} • {server['type']}</small>
                    </div>
                    <div>
                        <span style="color: {status_color[server['status']]}; font-size: 20px;">
                            {status_icon[server['status']]}
                        </span>
                    </div>
                </div>
                <div style="margin-top: 10px;">
                    <div style="display: flex; justify-content: space-between; font-size: 12px;">
                        <span>CPU: {server['cpu']}%</span>
                        <span>RAM: {server['memory']}%</span>
                    </div>
                    <div style="width: 100%; background: rgba(255,255,255,0.1); height: 4px; border-radius: 2px; margin-top: 5px;">
                        <div style="width: {server['cpu']}%; background: {status_color[server['status']]}; height: 100%; border-radius: 2px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Alerts
        st.subheader("Recent Alerts")

        alerts = [
            {"time": "10:23", "server": "CACHE-01", "message": "High CPU usage (82%)", "level": "warning"},
            {"time": "09:45", "server": "LB-01", "message": "Server is down", "level": "critical"},
            {"time": "08:15", "server": "WEB-01", "message": "High memory usage", "level": "warning"},
        ]

        for alert in alerts:
            level_color = "warning" if alert['level'] == 'warning' else "danger"
            st.markdown(f"""
            <div style="background: rgba(255, 193, 7, 0.1); padding: 10px; border-radius: 5px; margin-bottom: 5px; border-left: 3px solid #{'ffc107' if alert['level'] == 'warning' else 'ff4757'}">
                <small>
                    <strong>[{alert['time']}] {alert['server']}</strong><br>
                    {alert['message']}
                </small>
            </div>
            """, unsafe_allow_html=True)

    # Bottom section - Data Center Map
    st.markdown("---")
    st.subheader("Data Center Rack Layout")

    # Simulated rack view
    rack_data = {
        "Rack A": ["WEB-01", "WEB-02", "DB-01", "Empty"],
        "Rack B": ["CACHE-01", "CACHE-02", "LB-01", "Empty"],
        "Rack C": ["BACKUP-01", "MONITOR-01", "Empty", "Empty"],
    }

    rack_cols = st.columns(len(rack_data))

    for idx, (rack_name, servers_in_rack) in enumerate(rack_data.items()):
        with rack_cols[idx]:
            st.markdown(f"**{rack_name}**")
            for server in servers_in_rack:
                if server == "Empty":
                    bg_color = "#2d3748"
                    text_color = "#718096"
                else:
                    bg_color = "#1a365d"
                    text_color = "white"

                st.markdown(f"""
                <div style="background-color: {bg_color}; color: {text_color}; 
                          padding: 8px; margin: 2px 0; border-radius: 3px; 
                          text-align: center; font-size: 12px;">
                    {server}
                </div>
                """, unsafe_allow_html=True)

    # Auto-refresh every 5 seconds
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    time.sleep(5)
    st.rerun()


if __name__ == "__main__":
    main()