"""
Financial Immune System - Real-time Dashboard
============================================

A beautiful web dashboard for monitoring the Financial Immune System
with real-time visualizations inspired by biological immune systems.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

from immune_system_app import FinancialImmuneSystem, create_sample_transaction
from financial_immune_system import AnomalyType, ThreatLevel


# Configure Streamlit page
st.set_page_config(
    page_title="Financial Immune System",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state GLOBALLY before anything else
def initialize_session_state():
    """Initialize all session state variables - FORCE INITIALIZATION"""
    # Force initialization with setattr to ensure they exist
    for key, default_value in [
        ('transaction_log', []),
        ('threat_log', []),
        ('antibody_log', []),
        ('metrics_history', []),
        ('immune_system', None)
    ]:
        if not hasattr(st.session_state, key):
            setattr(st.session_state, key, default_value)

def ensure_session_state():
    """Ensure session state is initialized - call before any session_state access"""
    try:
        # Test if transaction_log exists
        _ = st.session_state.transaction_log
    except AttributeError:
        # Force re-initialization if it doesn't exist
        initialize_session_state()

# Call initialization immediately
initialize_session_state()

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .threat-alert {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .immune-status {
        background: linear-gradient(135deg, #26de81 0%, #20bf6b 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
</style>
""", unsafe_allow_html=True)


class ImmuneSystemDashboard:
    """Real-time dashboard for the Financial Immune System"""
    
    def __init__(self):
        # Session state is already initialized globally
        self.immune_system = st.session_state.immune_system
        self.transaction_log = st.session_state.transaction_log
        self.threat_log = st.session_state.threat_log
        self.antibody_log = st.session_state.antibody_log
        self.system_metrics_history = st.session_state.metrics_history
        
    async def initialize_system(self):
        """Initialize the immune system"""
        if st.session_state.immune_system is None:
            st.session_state.immune_system = FinancialImmuneSystem()
            await st.session_state.immune_system.start_system()
            
        self.immune_system = st.session_state.immune_system
    
    def render_header(self):
        """Render the main dashboard header"""
        st.markdown('<h1 class="main-header">🦠 Financial Immune System</h1>', unsafe_allow_html=True)
        st.markdown("### *Protecting your financial ecosystem like a biological immune system*")
        
        # Status indicator
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="immune-status">
                <h3>🛡️ System Status</h3>
                <h2>ACTIVE</h2>
                <p>All immune components operational</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>🔬 Detection Engines</h3>
                <h2>8 ACTIVE</h2>
                <p>White blood cells scanning</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>💉 Antibodies</h3>
                <h2>ADAPTIVE</h2>
                <p>Learning and evolving</p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with controls and information"""
        st.sidebar.markdown("## 🎛️ Control Panel")
        
        # System controls
        st.sidebar.markdown("### System Controls")
        
        if st.sidebar.button("🧪 Generate Test Transaction"):
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Create task for running event loop
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, self.generate_test_transaction())
                        future.result()
                else:
                    asyncio.run(self.generate_test_transaction())
            except Exception as e:
                st.error(f"Error generating transaction: {e}")
        
        if st.sidebar.button("🦠 Simulate Threat"):
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, self.simulate_threat())
                        future.result()
                else:
                    asyncio.run(self.simulate_threat())
            except Exception as e:
                st.error(f"Error simulating threat: {e}")
        
        if st.sidebar.button("🔄 Refresh System Status"):
            st.rerun()
        
        # Configuration
        st.sidebar.markdown("### ⚙️ Configuration")
        
        auto_generate = st.sidebar.checkbox("Auto-generate Antibodies", value=True)
        auto_distribute = st.sidebar.checkbox("Auto-distribute Immunity", value=True)
        real_time_monitoring = st.sidebar.checkbox("Real-time Monitoring", value=True)
        
        # Update system configuration
        if self.immune_system:
            self.immune_system.config.update({
                'auto_generate_antibodies': auto_generate,
                'auto_distribute_antibodies': auto_distribute,
                'real_time_monitoring': real_time_monitoring
            })
        
        # Threat simulation options
        st.sidebar.markdown("### 🎯 Threat Simulation")
        threat_type = st.sidebar.selectbox(
            "Threat Type",
            ["Velocity Attack", "Geographic Anomaly", "Amount Anomaly", "Account Takeover", "Card Testing"]
        )
        
        if st.sidebar.button("🚨 Launch Simulation"):
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, self.simulate_specific_threat(threat_type))
                        future.result()
                else:
                    asyncio.run(self.simulate_specific_threat(threat_type))
            except Exception as e:
                st.error(f"Error launching simulation: {e}")
        
        # System information
        st.sidebar.markdown("### 📊 System Info")
        if self.immune_system:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, self.immune_system.get_system_status())
                        status = future.result()
                else:
                    status = asyncio.run(self.immune_system.get_system_status())
                
                st.sidebar.metric("Uptime", f"{status['system_info']['uptime_seconds']:.0f}s")
                st.sidebar.metric("Transactions", status['performance_metrics']['transactions_processed'])
                st.sidebar.metric("Threats Detected", status['performance_metrics']['threats_detected'])
            except Exception as e:
                st.sidebar.error(f"Error getting status: {e}")
    
    async def generate_test_transaction(self):
        """Generate a normal test transaction"""
        if not self.immune_system:
            return
        
        # Ensure session state is initialized
        ensure_session_state()
        
        transaction = await create_sample_transaction()
        result = await self.immune_system.process_transaction(transaction)
        
        # Add to transaction log
        st.session_state.transaction_log.append({
            'timestamp': datetime.now(),
            'transaction': transaction,
            'result': result
        })
        
        # Keep only last 100 transactions
        if len(st.session_state.transaction_log) > 100:
            st.session_state.transaction_log = st.session_state.transaction_log[-100:]
        
        st.success(f"✅ Transaction processed: ${transaction.amount:.2f} - Status: {result['status']}")
    
    async def simulate_threat(self):
        """Simulate a random threat"""
        if not self.immune_system:
            return
        
        # Ensure session state is initialized
        ensure_session_state()
        
        threat_types = ["velocity", "geographic", "amount", "behavioral"]
        threat_type = np.random.choice(threat_types)
        
        await self.simulate_specific_threat(threat_type)
    
    async def simulate_specific_threat(self, threat_type: str):
        """Simulate a specific type of threat"""
        if not self.immune_system:
            return
        
        user_id = "test_user_123"
        
        if threat_type == "Velocity Attack" or threat_type == "velocity":
            # Generate multiple rapid transactions
            for i in range(15):
                transaction = await create_sample_transaction(
                    user_id=user_id,
                    amount=np.random.uniform(10, 100)
                )
                result = await self.immune_system.process_transaction(transaction)
                
                if result['threats_detected'] > 0:
                    st.session_state.threat_log.append({
                        'timestamp': datetime.now(),
                        'type': 'Velocity Attack',
                        'severity': 'HIGH',
                        'details': result
                    })
                    st.error(f"🚨 Velocity attack detected! {result['threats_detected']} threats found")
                    break
        
        elif threat_type == "Geographic Anomaly" or threat_type == "geographic":
            transaction = await create_sample_transaction(
                user_id=user_id,
                amount=2000,
                location="Unknown Location",
                merchant="Suspicious Merchant"
            )
            result = await self.immune_system.process_transaction(transaction)
            
            if result['threats_detected'] > 0:
                st.session_state.threat_log.append({
                    'timestamp': datetime.now(),
                    'type': 'Geographic Anomaly',
                    'severity': 'MEDIUM',
                    'details': result
                })
                st.warning(f"⚠️ Geographic anomaly detected! Risk score: {result['risk_score']}")
        
        elif threat_type == "Amount Anomaly" or threat_type == "amount":
            transaction = await create_sample_transaction(
                user_id=user_id,
                amount=75000  # Very large amount
            )
            result = await self.immune_system.process_transaction(transaction)
            
            if result['threats_detected'] > 0:
                st.session_state.threat_log.append({
                    'timestamp': datetime.now(),
                    'type': 'Amount Anomaly',
                    'severity': 'HIGH',
                    'details': result
                })
                st.error(f"🚨 Large amount anomaly detected! Status: {result['status']}")
        
        elif threat_type == "Account Takeover" or threat_type == "behavioral":
            # Simulate diverse transaction pattern
            locations = ["Tokyo", "London", "Sydney", "Mumbai"]
            merchants = ["Unknown1", "Suspicious2", "Fake3", "Test4"]
            
            for i in range(6):
                transaction = await create_sample_transaction(
                    user_id=user_id,
                    location=np.random.choice(locations),
                    merchant=np.random.choice(merchants),
                    amount=np.random.uniform(500, 3000)
                )
                result = await self.immune_system.process_transaction(transaction)
                
                if result['threats_detected'] > 0:
                    st.session_state.threat_log.append({
                        'timestamp': datetime.now(),
                        'type': 'Account Takeover',
                        'severity': 'CRITICAL',
                        'details': result
                    })
                    st.error(f"🚨 Account takeover pattern detected!")
                    break
        
        elif threat_type == "Card Testing":
            # Multiple small transactions
            for i in range(8):
                transaction = await create_sample_transaction(
                    user_id=user_id,
                    amount=np.random.uniform(1, 10)
                )
                result = await self.immune_system.process_transaction(transaction)
                
                if result['threats_detected'] > 0:
                    st.session_state.threat_log.append({
                        'timestamp': datetime.now(),
                        'type': 'Card Testing',
                        'severity': 'HIGH',
                        'details': result
                    })
                    st.error(f"🚨 Card testing attack detected!")
                    break
    
    def render_real_time_metrics(self):
        """Render real-time system metrics"""
        st.markdown("## 📊 Real-time System Metrics")
        
        if not self.immune_system:
            st.warning("⚠️ Immune system not initialized")
            return
        
        # Get current system status
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.immune_system.get_system_status())
                    status = future.result()
            else:
                status = asyncio.run(self.immune_system.get_system_status())
        except Exception as e:
            st.error(f"Error getting system status: {e}")
            return
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Transactions Processed",
                status['performance_metrics']['transactions_processed'],
                delta=1 if st.session_state.transaction_log else 0
            )
        
        with col2:
            st.metric(
                "Threats Detected",
                status['performance_metrics']['threats_detected'],
                delta=1 if st.session_state.threat_log else 0
            )
        
        with col3:
            st.metric(
                "Active Antibodies",
                status['active_antibodies_count'],
                delta=0
            )
        
        with col4:
            network_health = status['network_status']['network_health']
            st.metric(
                "Network Health",
                f"{network_health:.1%}",
                delta=f"{network_health - 0.95:.1%}" if network_health < 0.95 else "Optimal"
            )
        
        # Store metrics history
        st.session_state.metrics_history.append({
            'timestamp': datetime.now(),
            'transactions': status['performance_metrics']['transactions_processed'],
            'threats': status['performance_metrics']['threats_detected'],
            'antibodies': status['active_antibodies_count'],
            'network_health': network_health
        })
        
        # Keep only last 100 data points
        if len(st.session_state.metrics_history) > 100:
            st.session_state.metrics_history = st.session_state.metrics_history[-100:]
    
    def render_threat_visualization(self):
        """Render threat detection visualization"""
        st.markdown("## 🦠 Threat Detection Visualization")
        
        if not st.session_state.threat_log:
            st.info("No threats detected yet. Use the sidebar to simulate threats.")
            return
        
        # Create threat timeline
        threat_df = pd.DataFrame([
            {
                'timestamp': threat['timestamp'],
                'type': threat['type'],
                'severity': threat['severity'],
                'risk_score': threat['details'].get('risk_score', 0)
            }
            for threat in st.session_state.threat_log[-20:]  # Last 20 threats
        ])
        
        # Threat timeline chart
        fig = px.scatter(
            threat_df,
            x='timestamp',
            y='risk_score',
            color='severity',
            size='risk_score',
            hover_data=['type'],
            title="Threat Detection Timeline",
            color_discrete_map={
                'LOW': '#28a745',
                'MEDIUM': '#ffc107',
                'HIGH': '#fd7e14',
                'CRITICAL': '#dc3545'
            }
        )
        
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Risk Score",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Threat type distribution
        col1, col2 = st.columns(2)
        
        with col1:
            threat_counts = threat_df['type'].value_counts()
            fig_pie = px.pie(
                values=threat_counts.values,
                names=threat_counts.index,
                title="Threat Types Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            severity_counts = threat_df['severity'].value_counts()
            fig_bar = px.bar(
                x=severity_counts.index,
                y=severity_counts.values,
                title="Threat Severity Distribution",
                color=severity_counts.index,
                color_discrete_map={
                    'LOW': '#28a745',
                    'MEDIUM': '#ffc107',
                    'HIGH': '#fd7e14',
                    'CRITICAL': '#dc3545'
                }
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    def render_immune_network(self):
        """Render immune system network visualization"""
        st.markdown("## 🕸️ Immune Network Topology")
        
        if not self.immune_system:
            return
        
        # Get network status
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.immune_system.distribution_network.get_network_status())
                    network_status = future.result()
            else:
                network_status = asyncio.run(self.immune_system.distribution_network.get_network_status())
        except Exception as e:
            st.error(f"Error getting network status: {e}")
            return
        
        # Create network visualization
        nodes = list(self.immune_system.distribution_network.network_nodes.keys())
        
        if not nodes:
            st.info("No network nodes registered yet.")
            return
        
        # Create a simple network graph
        fig = go.Figure()
        
        # Add nodes
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        
        # Arrange nodes in a circle
        n_nodes = len(nodes)
        for i, node in enumerate(nodes):
            angle = 2 * np.pi * i / n_nodes
            x = np.cos(angle)
            y = np.sin(angle)
            
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            
            # Color based on health
            node_info = self.immune_system.distribution_network.network_nodes[node]
            if node_info['health_status'] == 'healthy':
                node_colors.append('#28a745')
            else:
                node_colors.append('#dc3545')
        
        # Add edges (connections between all nodes)
        edge_x = []
        edge_y = []
        
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                edge_x.extend([node_x[i], node_x[j], None])
                edge_y.extend([node_y[i], node_y[j], None])
        
        # Add edges to plot
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='rgba(125, 125, 125, 0.3)'),
            hoverinfo='none',
            mode='lines'
        ))
        
        # Add nodes to plot
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            marker=dict(
                size=30,
                color=node_colors,
                line=dict(width=2, color='white')
            )
        ))
        
        fig.update_layout(
            title="Immune System Network Topology",
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="Green: Healthy Nodes, Red: Error Nodes",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor='left', yanchor='bottom',
                font=dict(color='gray', size=12)
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Network statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Nodes", network_status['total_nodes'])
        
        with col2:
            st.metric("Healthy Nodes", network_status['healthy_nodes'])
        
        with col3:
            st.metric("Network Health", f"{network_status['network_health']:.1%}")
    
    def render_antibody_evolution(self):
        """Render antibody evolution and adaptation"""
        st.markdown("## 💉 Antibody Evolution & Adaptation")
        
        if not self.immune_system or not self.immune_system.active_antibodies:
            st.info("No antibodies generated yet. Simulate threats to see antibody creation.")
            return
        
        # Display active antibodies
        antibodies_data = []
        for antibody_id, antibody in self.immune_system.active_antibodies.items():
            antibodies_data.append({
                'ID': antibody_id[:8],
                'Name': antibody.name,
                'Type': antibody.rule_logic.get('type', 'unknown'),
                'Effectiveness': f"{antibody.effectiveness_score:.2%}",
                'Activations': antibody.activation_count,
                'Created': antibody.creation_timestamp.strftime('%H:%M:%S'),
                'Last Updated': antibody.last_updated.strftime('%H:%M:%S')
            })
        
        if antibodies_data:
            df = pd.DataFrame(antibodies_data)
            st.dataframe(df, use_container_width=True)
            
            # Effectiveness chart
            fig = px.bar(
                df,
                x='Name',
                y=[float(x.strip('%'))/100 for x in df['Effectiveness']],
                title="Antibody Effectiveness Scores",
                color=[float(x.strip('%'))/100 for x in df['Effectiveness']],
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(yaxis_title="Effectiveness Score", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Immune memory statistics
        memory_stats = len(self.immune_system.immune_memory.memory_store)
        st.metric("Immune Memory Entries", memory_stats)
    
    def render_transaction_log(self):
        """Render recent transaction log"""
        st.markdown("## 📝 Recent Transaction Log")
        
        # Ensure session state is initialized
        ensure_session_state()
        
        if not st.session_state.transaction_log:
            st.info("No transactions processed yet. Use the sidebar to generate test transactions.")
            return
        
        # Display recent transactions
        recent_transactions = st.session_state.transaction_log[-10:]  # Last 10 transactions
        
        transaction_data = []
        for log_entry in recent_transactions:
            transaction = log_entry['transaction']
            result = log_entry['result']
            
            transaction_data.append({
                'Time': log_entry['timestamp'].strftime('%H:%M:%S'),
                'User ID': transaction.user_id[:12] + '...',
                'Amount': f"${transaction.amount:.2f}",
                'Location': transaction.location,
                'Merchant': transaction.merchant,
                'Status': result['status'],
                'Threats': result['threats_detected'],
                'Risk Score': f"{result.get('risk_score', 0):.1f}",
                'Processing Time': f"{result['processing_time']:.3f}s"
            })
        
        df = pd.DataFrame(transaction_data)
        
        # Color code by status
        def highlight_status(val):
            if val == 'blocked':
                return 'background-color: #ffebee'
            elif val == 'flagged':
                return 'background-color: #fff3e0'
            elif val == 'approved_with_conditions':
                return 'background-color: #f3e5f5'
            else:
                return 'background-color: #e8f5e8'
        
        styled_df = df.style.applymap(highlight_status, subset=['Status'])
        st.dataframe(styled_df, use_container_width=True)
    
    async def run_dashboard(self):
        """Run the main dashboard"""
        # Initialize system
        await self.initialize_system()
        
        # Render components
        self.render_header()
        self.render_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Metrics", "🦠 Threats", "🕸️ Network", "💉 Antibodies", "📝 Transactions"
        ])
        
        with tab1:
            self.render_real_time_metrics()
        
        with tab2:
            self.render_threat_visualization()
        
        with tab3:
            self.render_immune_network()
        
        with tab4:
            self.render_antibody_evolution()
        
        with tab5:
            self.render_transaction_log()
        
        # Auto-refresh option
        if st.checkbox("🔄 Auto-refresh (5 seconds)", value=False):
            time.sleep(5)
            st.rerun()


def main():
    """Main function to run the dashboard"""
    # Ensure session state is initialized
    initialize_session_state()
    dashboard = ImmuneSystemDashboard()
    
    # Run the dashboard
    try:
        # Check if we're in an existing event loop
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're in Streamlit's event loop, run synchronously
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, dashboard.run_dashboard())
                    future.result()
            else:
                asyncio.run(dashboard.run_dashboard())
        except RuntimeError:
            # No event loop, create one
            asyncio.run(dashboard.run_dashboard())
    except Exception as e:
        st.error(f"Error running dashboard: {e}")
        st.info("Please refresh the page to restart the system.")


if __name__ == "__main__":
    import time
    main()
