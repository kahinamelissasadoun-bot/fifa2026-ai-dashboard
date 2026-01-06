"""
FIFA World Cup 2026 - Multi-Agent Crisis Management System
Advanced AI Dashboard with Agent Communication Network Visualization
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
from datetime import datetime
import json

st.set_page_config(
    page_title="FIFA 2026 AI Crisis Manager",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .header-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .header-title {
        color: white;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        color: #b8c5d6;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .timeline-item {
        padding: 1rem;
        border-left: 3px solid #667eea;
        margin-left: 1rem;
        margin-bottom: 1rem;
        background: #f8fafc;
        border-radius: 0 8px 8px 0;
    }
    
    .message-log {
        background: #1e293b;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 1rem;
    }
    
    .message-line {
        padding: 0.3rem 0;
        border-bottom: 1px solid #334155;
    }
    
    .message-request {
        color: #fbbf24;
    }
    
    .message-response {
        color: #34d399;
    }
    
    .message-transfer {
        color: #60a5fa;
    }
    
    .message-alert {
        color: #f87171;
    }
    
    .agent-status-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        margin-bottom: 0.5rem;
    }
    
    .badge-active {
        background: #d1fae5;
        color: #059669;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-inactive {
        background: #fee2e2;
        color: #dc2626;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .communication-stats {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class Message:
    def __init__(self, msg_type, sender, receiver, content, timestamp):
        self.type = msg_type
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = timestamp

class EnvironmentHybrid:
    def __init__(self, cities_data):
        self.cities = list(cities_data.keys())
        self.dynamic_state = {}
        self.messages_log = []
        
        for city, data in cities_data.items():
            self.dynamic_state[city] = {
                'occupancy_rate': data['occupancy'],
                'crisis_level': 0.0,
                'available_rooms': data['capacity'],
                'stress_level': 'BAS',
                'resources_received': 0,
                'resources_given': 0,
                'cluster': data['cluster'],
                'popularity_rank': data['popularity'],
                'num_matches': data['matches'],
                'capacity': data['capacity'],
                'messages_sent': 0,
                'messages_received': 0
            }
    
    def log_message(self, msg):
        self.messages_log.append(msg)
    
    def get_city_state(self, city):
        occ = self.dynamic_state[city]['occupancy_rate']
        capacity = self.dynamic_state[city]['capacity']
        
        if occ >= 0.85:
            stress = 'CRITICAL'
            crisis = 0.9
        elif occ >= 0.70:
            stress = 'HIGH'
            crisis = 0.7
        elif occ >= 0.50:
            stress = 'MEDIUM'
            crisis = 0.4
        else:
            stress = 'LOW'
            crisis = 0.1
        
        self.dynamic_state[city]['stress_level'] = stress
        self.dynamic_state[city]['crisis_level'] = crisis
        self.dynamic_state[city]['available_rooms'] = int(capacity * (1 - occ))
        
        return {
            'city': city,
            'occupancy_rate': occ,
            'crisis_level': crisis,
            'available_rooms': self.dynamic_state[city]['available_rooms'],
            'stress_level': stress,
            'cluster': self.dynamic_state[city]['cluster'],
            'popularity_rank': self.dynamic_state[city]['popularity_rank'],
            'resources_received': self.dynamic_state[city]['resources_received'],
            'resources_given': self.dynamic_state[city]['resources_given'],
            'num_matches': self.dynamic_state[city]['num_matches'],
            'capacity': capacity,
            'messages_sent': self.dynamic_state[city]['messages_sent'],
            'messages_received': self.dynamic_state[city]['messages_received']
        }

class BayesianCrisisPredictor:
    def __init__(self):
        self.rules_applied = {}
    
    def predict_crisis_probability(self, city_state):
        occ = city_state['occupancy_rate']
        cluster_score = 0.60 if city_state['cluster'] == 0 else 0.40
        hadoop_score = 0.55 + (city_state['num_matches'] / 12) * 0.1
        crisis_prob = 0.60 * occ + 0.20 * hadoop_score + 0.20 * cluster_score
        return np.clip(crisis_prob, 0.0, 1.0)
    
    def classify_risk_ml(self, city_state):
        occ = city_state['occupancy_rate']
        if occ >= 0.75:
            return 'HIGH_RISK'
        elif occ >= 0.50:
            return 'MEDIUM_RISK'
        else:
            return 'LOW_RISK'
    
    def get_recommendations(self, city_state):
        crisis_prob = self.predict_crisis_probability(city_state)
        ml_class = self.classify_risk_ml(city_state)
        
        if crisis_prob >= 0.75:
            return "CRITICAL: Immediate coordinator intervention required"
        elif crisis_prob >= 0.60:
            return "HIGH RISK: Request assistance from helper cities"
        elif crisis_prob >= 0.45:
            return "MODERATE: Optimize local resources and monitor closely"
        else:
            return "STABLE: Resources available to assist other cities"

class AgentCoordinator:
    def __init__(self):
        self.interventions = 0
        self.crises_resolved = 0
        self.transfers_log = []
        self.decisions_log = []
        self.communication_graph = {'nodes': [], 'edges': []}
        self.messages_sent = 0
        self.messages_received = 0
    
    def detect_and_coordinate(self, env, bayesian):
        crises = []
        helpers = []
        
        for city in env.cities:
            state = env.get_city_state(city)
            crisis_prob = bayesian.predict_crisis_probability(state)
            
            msg = Message(
                'PERCEPTION',
                city,
                'Coordinator',
                f"Status report: Occ={state['occupancy_rate']:.2f}, Crisis={crisis_prob:.2f}",
                datetime.now()
            )
            env.log_message(msg)
            env.dynamic_state[city]['messages_sent'] += 1
            self.messages_received += 1
            
            if crisis_prob >= 0.68 or state['occupancy_rate'] >= 0.78:
                crises.append((city, crisis_prob, state['occupancy_rate']))
                
                alert_msg = Message(
                    'ALERT',
                    city,
                    'Coordinator',
                    f"CRISIS ALERT: Immediate assistance required",
                    datetime.now()
                )
                env.log_message(alert_msg)
                env.dynamic_state[city]['messages_sent'] += 1
                self.messages_received += 1
                
            elif crisis_prob < 0.52 and state['occupancy_rate'] < 0.60:
                helpers.append((city, state['available_rooms']))
                
                offer_msg = Message(
                    'OFFER',
                    city,
                    'Coordinator',
                    f"Available to help: {state['available_rooms']:,} rooms free",
                    datetime.now()
                )
                env.log_message(offer_msg)
                env.dynamic_state[city]['messages_sent'] += 1
                self.messages_received += 1
        
        if len(crises) > 0 and len(helpers) > 0:
            decision_msg = Message(
                'DECISION',
                'Coordinator',
                'ALL',
                f"Initiating coordination: {len(crises)} crises, {len(helpers)} helpers",
                datetime.now()
            )
            env.log_message(decision_msg)
            self.messages_sent += 1
            
            for crisis_city, crisis_prob, crisis_occ in crises[:2]:
                if helpers:
                    helper_city, helper_rooms = helpers[0]
                    reduction = 0.15 if len(crises) > 1 else 0.18
                    
                    request_msg = Message(
                        'REQUEST',
                        'Coordinator',
                        helper_city,
                        f"Transfer {reduction*100:.0f}% capacity to {crisis_city}",
                        datetime.now()
                    )
                    env.log_message(request_msg)
                    self.messages_sent += 1
                    env.dynamic_state[helper_city]['messages_received'] += 1
                    
                    self.transfer_resources(env, helper_city, crisis_city, reduction)
                    
                    confirm_msg = Message(
                        'TRANSFER',
                        helper_city,
                        crisis_city,
                        f"Resources transferred: {reduction*100:.0f}% capacity",
                        datetime.now()
                    )
                    env.log_message(confirm_msg)
                    env.dynamic_state[helper_city]['messages_sent'] += 1
                    env.dynamic_state[crisis_city]['messages_received'] += 1
                    
                    self.transfers_log.append({
                        'from': helper_city,
                        'to': crisis_city,
                        'reduction': reduction,
                        'crisis_prob': crisis_prob
                    })
                    self.interventions += 1
                    
                    self.communication_graph['edges'].append({
                        'from': helper_city,
                        'to': crisis_city,
                        'type': 'transfer',
                        'weight': reduction
                    })
            
            self.crises_resolved = len(crises)
        
        for city in env.cities:
            self.communication_graph['nodes'].append({
                'id': city,
                'type': 'agent',
                'status': env.get_city_state(city)['stress_level']
            })
        
        self.communication_graph['nodes'].append({
            'id': 'Coordinator',
            'type': 'coordinator',
            'status': 'ACTIVE'
        })
        
        for city in env.cities:
            self.communication_graph['edges'].append({
                'from': city,
                'to': 'Coordinator',
                'type': 'report',
                'weight': 1
            })
        
        return len(crises), len(helpers), crises, helpers
    
    def transfer_resources(self, env, from_city, to_city, reduction):
        current_occ = env.dynamic_state[to_city]['occupancy_rate']
        new_occ = max(0.30, current_occ - reduction)
        env.dynamic_state[to_city]['occupancy_rate'] = new_occ
        
        capacity = env.dynamic_state[to_city]['capacity']
        resources = int(capacity * reduction)
        env.dynamic_state[to_city]['resources_received'] += resources
        env.dynamic_state[from_city]['resources_given'] += resources

def calculate_system_score(env):
    total = 0
    for city in env.cities:
        state = env.get_city_state(city)
        occ = state['occupancy_rate']
        
        if 0.40 <= occ <= 0.65:
            occ_score = 12
        elif 0.30 <= occ <= 0.75:
            occ_score = 9
        else:
            occ_score = 5
        
        crisis_score = 10 if state['crisis_level'] < 0.30 else 7 if state['crisis_level'] < 0.60 else 3
        total += occ_score + crisis_score
    
    return int((total / (22 * len(env.cities))) * 100)

def create_agent_network_graph(coordinator, env):
    G = nx.DiGraph()
    
    G.add_node('Coordinator', node_type='coordinator')
    for city in env.cities:
        state = env.get_city_state(city)
        G.add_node(city, node_type='agent', stress=state['stress_level'])
    
    for edge in coordinator.communication_graph['edges']:
        G.add_edge(edge['from'], edge['to'], 
                  edge_type=edge['type'], 
                  weight=edge.get('weight', 1))
    
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    edge_trace_report = []
    edge_trace_transfer = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        edge_type = edge[2].get('edge_type', 'report')
        
        if edge_type == 'transfer':
            edge_trace_transfer.append(
                go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode='lines',
                    line=dict(width=4, color='#f59e0b'),
                    hoverinfo='none',
                    showlegend=False
                )
            )
        else:
            edge_trace_report.append(
                go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode='lines',
                    line=dict(width=2, color='#94a3b8', dash='dot'),
                    hoverinfo='none',
                    showlegend=False
                )
            )
    
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    
    for node in G.nodes(data=True):
        x, y = pos[node[0]]
        node_x.append(x)
        node_y.append(y)
        
        if node[1].get('node_type') == 'coordinator':
            node_text.append('COORDINATOR')
            node_color.append('#667eea')
            node_size.append(50)
        else:
            state = env.get_city_state(node[0])
            node_text.append(f"{node[0].replace('_', ' ')}<br>Occ: {state['occupancy_rate']*100:.1f}%")
            
            if state['stress_level'] in ['CRITICAL', 'HIGH']:
                node_color.append('#dc2626')
            elif state['stress_level'] == 'MEDIUM':
                node_color.append('#d97706')
            else:
                node_color.append('#059669')
            
            node_size.append(35)
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=2, color='white')
        ),
        text=node_text,
        textposition='top center',
        textfont=dict(size=10, color='#1e293b', family='Inter'),
        hoverinfo='text'
    )
    
    fig = go.Figure(data=edge_trace_report + edge_trace_transfer + [node_trace])
    
    fig.update_layout(
        title='Agent Communication Network',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=500,
        plot_bgcolor='#f8fafc',
        font=dict(family='Inter, sans-serif')
    )
    
    return fig

def create_communication_flow_chart(messages_log):
    if not messages_log:
        return go.Figure()
    
    message_types = ['PERCEPTION', 'ALERT', 'OFFER', 'DECISION', 'REQUEST', 'TRANSFER']
    counts = {mt: 0 for mt in message_types}
    
    for msg in messages_log:
        if msg.type in counts:
            counts[msg.type] += 1
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(counts.keys()),
            y=list(counts.values()),
            marker_color=['#3b82f6', '#ef4444', '#10b981', '#8b5cf6', '#f59e0b', '#06b6d4'],
            text=list(counts.values()),
            textposition='outside',
            textfont=dict(size=14, weight=600)
        )
    ])
    
    fig.update_layout(
        title='Message Distribution by Type',
        xaxis_title='Message Type',
        yaxis_title='Count',
        height=350,
        template='plotly_white',
        font=dict(family='Inter, sans-serif')
    )
    
    return fig

def create_comparison_chart(before_data, after_data, cities):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Before Coordination',
        x=cities,
        y=before_data,
        marker_color='#ff6b6b',
        text=[f'{val:.1f}%' for val in before_data],
        textposition='outside',
        textfont=dict(size=12, color='#1e293b', weight=600)
    ))
    
    fig.add_trace(go.Bar(
        name='After Coordination',
        x=cities,
        y=after_data,
        marker_color='#51cf66',
        text=[f'{val:.1f}%' for val in after_data],
        textposition='outside',
        textfont=dict(size=12, color='#1e293b', weight=600)
    ))
    
    fig.add_hline(y=78, line_dash="dash", line_color="red", 
                  annotation_text="Crisis Threshold", annotation_position="right")
    fig.add_hline(y=60, line_dash="dot", line_color="orange",
                  annotation_text="Warning Level", annotation_position="right")
    
    fig.update_layout(
        barmode='group',
        title=dict(text='Occupancy Rate: Before vs After Coordination', 
                  font=dict(size=18, weight=600)),
        xaxis_title='City',
        yaxis_title='Occupancy Rate (%)',
        height=450,
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Inter, sans-serif")
    )
    
    return fig

def create_crisis_heatmap(env, bayesian):
    cities = env.cities
    metrics = ['Occupancy', 'Crisis Probability', 'Stress Level']
    
    data = []
    for city in cities:
        state = env.get_city_state(city)
        crisis_prob = bayesian.predict_crisis_probability(state)
        stress_map = {'LOW': 0.2, 'MEDIUM': 0.5, 'HIGH': 0.75, 'CRITICAL': 0.95}
        
        data.append([
            state['occupancy_rate'],
            crisis_prob,
            stress_map.get(state['stress_level'], 0.5)
        ])
    
    fig = go.Figure(data=go.Heatmap(
        z=np.array(data).T,
        x=[c.replace('_', ' ') for c in cities],
        y=metrics,
        colorscale='RdYlGn_r',
        text=[[f'{val:.2f}' for val in row] for row in np.array(data).T],
        texttemplate='%{text}',
        textfont={"size": 14, "weight": 600},
        colorbar=dict(title="Risk Level")
    ))
    
    fig.update_layout(
        title='Multi-Dimensional Risk Assessment Heatmap',
        height=300,
        template='plotly_white',
        font=dict(family="Inter, sans-serif", size=12)
    )
    
    return fig

def create_score_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "System Performance", 'font': {'size': 20, 'weight': 600}},
        delta={'reference': 70, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "darkblue"},
            'bar': {'color': "#667eea", 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#fee2e2'},
                {'range': [50, 75], 'color': '#fef3c7'},
                {'range': [75, 100], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300, template='plotly_white',
                     font=dict(family="Inter, sans-serif"))
    
    return fig

def create_agent_performance_chart(env, bayesian):
    agents_data = []
    
    for city in env.cities:
        state = env.get_city_state(city)
        crisis_prob = bayesian.predict_crisis_probability(state)
        ml_class = bayesian.classify_risk_ml(state)
        
        utility = 10 if state['occupancy_rate'] < 0.45 else \
                  7 if 0.45 <= state['occupancy_rate'] < 0.65 else \
                  5 if 0.65 <= state['occupancy_rate'] < 0.78 else 13
        
        agents_data.append({
            'Agent': city.replace('_', ' '),
            'Utility Score': utility,
            'Crisis Probability': crisis_prob * 100,
            'ML Classification': ml_class,
            'Status': state['stress_level']
        })
    
    df = pd.DataFrame(agents_data)
    
    fig = go.Figure()
    
    colors = {'HIGH_RISK': '#dc2626', 'MEDIUM_RISK': '#d97706', 'LOW_RISK': '#059669'}
    
    for ml_class in df['ML Classification'].unique():
        df_class = df[df['ML Classification'] == ml_class]
        fig.add_trace(go.Bar(
            name=ml_class,
            x=df_class['Agent'],
            y=df_class['Utility Score'],
            marker_color=colors.get(ml_class, '#64748b'),
            text=df_class['Utility Score'],
            textposition='outside'
        ))
    
    fig.update_layout(
        title='Agent Utility Scores by Risk Classification',
        xaxis_title='City Agent',
        yaxis_title='Utility Score',
        height=400,
        template='plotly_white',
        barmode='group',
        font=dict(family="Inter, sans-serif")
    )
    
    return fig

def main():
    st.markdown("""
    <div class="header-container">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 class="header-title">FIFA World Cup 2026</h1>
                <p class="header-subtitle">AI-Powered Multi-Agent Crisis Management System</p>
            </div>
            <div>
                <svg class="fifa-logo" width="120" height="60" viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
                    <text x="10" y="60" font-family="Arial Black" font-size="50" font-weight="bold" fill="white">FIFA</text>
                    <text x="10" y="85" font-family="Arial" font-size="20" fill="#b8c5d6">2026</text>
                </svg>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("## ⚙️ Configuration Panel")
    st.sidebar.markdown("### City Occupancy Parameters")
    
    cities_config = {}
    default_values = {
        'Los_Angeles': 0.60,
        'Mexico_City': 0.47,
        'New_York': 0.48,
        'Toronto': 0.84
    }
    
    for city, default in default_values.items():
        cities_config[city] = st.sidebar.slider(
            f"{city.replace('_', ' ')}",
            min_value=0.30,
            max_value=0.95,
            value=default,
            step=0.01,
            format="%.2f"
        )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### System Configuration")
    
    use_coordinator = st.sidebar.checkbox("Enable Coordinator Agent", value=True)
    show_messages = st.sidebar.checkbox("Show Communication Log", value=True)
    num_cycles = st.sidebar.selectbox("Simulation Cycles", [1, 2, 3], index=1)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Scenarios")
    
    col1, col2, col3 = st.sidebar.columns(3)
    
    if col1.button("Normal"):
        for key in cities_config:
            cities_config[key] = np.random.uniform(0.45, 0.65)
        st.rerun()
    
    if col2.button("Warning"):
        cities_config['Los_Angeles'] = 0.72
        cities_config['Toronto'] = 0.68
        st.rerun()
    
    if col3.button("Crisis"):
        cities_config['Los_Angeles'] = 0.88
        cities_config['Toronto'] = 0.91
        cities_config['New_York'] = 0.42
        cities_config['Mexico_City'] = 0.39
        st.rerun()
    
    st.sidebar.markdown("---")
    run_button = st.sidebar.button("▶ RUN SIMULATION", type="primary")
    
    if run_button or 'initialized' not in st.session_state:
        st.session_state.initialized = True
        
        with st.spinner("Initializing multi-agent system..."):
            cities_data = {
                'Los_Angeles': {
                    'occupancy': cities_config['Los_Angeles'],
                    'capacity': 6659579,
                    'cluster': 1,
                    'popularity': 2,
                    'matches': 8
                },
                'Mexico_City': {
                    'occupancy': cities_config['Mexico_City'],
                    'capacity': 3736279,
                    'cluster': 0,
                    'popularity': 3,
                    'matches': 6
                },
                'New_York': {
                    'occupancy': cities_config['New_York'],
                    'capacity': 7240856,
                    'cluster': 1,
                    'popularity': 1,
                    'matches': 10
                },
                'Toronto': {
                    'occupancy': cities_config['Toronto'],
                    'capacity': 2598127,
                    'cluster': 0,
                    'popularity': 4,
                    'matches': 8
                }
            }
            
            env = EnvironmentHybrid(cities_data)
            bayesian = BayesianCrisisPredictor()
            coordinator = AgentCoordinator()
            
            before_occupancy = [env.dynamic_state[city]['occupancy_rate'] * 100 
                              for city in env.cities]
            score_initial = calculate_system_score(env)
            
            crises_detected = 0
            helpers_available = 0
            crises_list = []
            helpers_list = []
            
            if use_coordinator:
                crises_detected, helpers_available, crises_list, helpers_list = \
                    coordinator.detect_and_coordinate(env, bayesian)
            
            after_occupancy = [env.dynamic_state[city]['occupancy_rate'] * 100 
                             for city in env.cities]
            score_final = calculate_system_score(env)
            
            total_messages = len(env.messages_log)
            
            st.session_state.results = {
                'env': env,
                'coordinator': coordinator,
                'bayesian': bayesian,
                'score_initial': score_initial,
                'score_final': score_final,
                'crises_detected': crises_detected,
                'helpers_available': helpers_available,
                'use_coordinator': use_coordinator,
                'before_occupancy': before_occupancy,
                'after_occupancy': after_occupancy,
                'crises_list': crises_list,
                'helpers_list': helpers_list,
                'total_messages': total_messages
            }
    
    if 'results' in st.session_state:
        results = st.session_state.results
        env = results['env']
        coordinator = results['coordinator']
        bayesian = results['bayesian']
        
        st.markdown('<p class="section-header">📊 System Performance Dashboard</p>', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            delta = results['score_final'] - results['score_initial']
            st.metric("System Score", 
                     f"{results['score_final']}/100",
                     f"{delta:+d} pts")
        
        with col2:
            st.metric("Crises Detected", results['crises_detected'])
        
        with col3:
            st.metric("Helper Cities", results['helpers_available'])
        
        with col4:
            if results['use_coordinator']:
                st.metric("Crises Resolved", coordinator.crises_resolved)
            else:
                st.metric("Coordinator", "OFF")
        
        with col5:
            st.metric("Transfers", len(coordinator.transfers_log))
        
        with col6:
            st.metric("Messages", results['total_messages'])
        
        st.markdown("---")
        
        if results['use_coordinator']:
            st.markdown('<p class="section-header">🔗 Agent Communication Network</p>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.plotly_chart(create_agent_network_graph(coordinator, env), 
                              use_container_width=True)
                
                st.markdown("""
                **Legend:**
                - **Purple Node**: Coordinator (central orchestrator)
                - **Green Nodes**: Stable agents (can offer help)
                - **Orange Nodes**: Warning level agents
                - **Red Nodes**: Crisis agents (need assistance)
                - **Dotted Lines**: Status reports to coordinator
                - **Solid Orange Lines**: Resource transfers
                """)
            
            with col2:
                st.plotly_chart(create_communication_flow_chart(env.messages_log),
                              use_container_width=True)
                
                st.markdown(f"""
                <div class="communication-stats">
                    <h3>Communication Statistics</h3>
                    <p style="font-size: 2rem; margin: 0.5rem 0;">{results['total_messages']}</p>
                    <p style="font-size: 0.9rem; margin: 0;">Total Messages Exchanged</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("##### Agent Activity")
                for city in env.cities:
                    state = env.get_city_state(city)
                    st.markdown(f"""
                    <div class="agent-status-card">
                        <strong>{city.replace('_', ' ')}</strong>
                        <span class="badge-{'active' if state['messages_sent'] > 0 else 'inactive'}">
                            {'ACTIVE' if state['messages_sent'] > 0 else 'IDLE'}
                        </span>
                        <br>
                        <small>Sent: {state['messages_sent']} | Received: {state['messages_received']}</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        if show_messages and env.messages_log:
            st.markdown('<p class="section-header">📝 Real-Time Communication Log</p>', unsafe_allow_html=True)
            
            log_html = '<div class="message-log">'
            for msg in env.messages_log[-20:]:
                msg_class = f"message-{msg.type.lower()}"
                timestamp = msg.timestamp.strftime("%H:%M:%S")
                log_html += f'<div class="message-line {msg_class}">'
                log_html += f'[{timestamp}] <strong>{msg.type}</strong> | '
                log_html += f'{msg.sender} → {msg.receiver}: {msg.content}'
                log_html += '</div>'
            log_html += '</div>'
            
            st.markdown(log_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.plotly_chart(
                create_comparison_chart(
                    results['before_occupancy'],
                    results['after_occupancy'],
                    [c.replace('_', ' ') for c in env.cities]
                ),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(create_score_gauge(results['score_final']), 
                          use_container_width=True)
        
        st.markdown('<p class="section-header">🎯 AI Analysis & Predictions</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_crisis_heatmap(env, bayesian), 
                          use_container_width=True)
        
        with col2:
            st.plotly_chart(create_agent_performance_chart(env, bayesian),
                          use_container_width=True)
        
        st.markdown('<p class="section-header">🏙️ Detailed City Analysis</p>', unsafe_allow_html=True)
        
        for city in env.cities:
            state = env.get_city_state(city)
            crisis_prob = bayesian.predict_crisis_probability(state)
            ml_class = bayesian.classify_risk_ml(state)
            recommendation = bayesian.get_recommendations(state)
            
            with st.expander(f"🏙️ {city.replace('_', ' ')} - {state['stress_level']} STATUS", expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Occupancy Rate", f"{state['occupancy_rate']*100:.1f}%")
                
                with col2:
                    st.metric("Crisis Probability", f"{crisis_prob*100:.1f}%")
                
                with col3:
                    st.metric("Available Rooms", f"{state['available_rooms']:,}")
                
                with col4:
                    st.metric("ML Classification", ml_class)
                
                st.markdown(f"**AI Recommendation:** {recommendation}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Messages Sent:** {state['messages_sent']}")
                with col2:
                    st.markdown(f"**Messages Received:** {state['messages_received']}")
                
                if state['resources_received'] > 0:
                    st.success(f"✓ Received {state['resources_received']:,} rooms from helper cities")
                if state['resources_given'] > 0:
                    st.info(f"→ Provided {state['resources_given']:,} rooms to crisis cities")
        
        if results['use_coordinator'] and coordinator.transfers_log:
            st.markdown('<p class="section-header">🔄 Coordination Timeline</p>', unsafe_allow_html=True)
            
            for i, transfer in enumerate(coordinator.transfers_log, 1):
                st.markdown(f"""
                <div class="timeline-item">
                    <strong>Transfer #{i}</strong><br>
                    From: <strong>{transfer['from'].replace('_', ' ')}</strong> → 
                    To: <strong>{transfer['to'].replace('_', ' ')}</strong><br>
                    Reduction: <strong>{transfer['reduction']*100:.0f}%</strong> | 
                    Crisis Probability: <strong>{transfer['crisis_prob']*100:.1f}%</strong>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<p class="section-header">📈 Detailed Statistics</p>', unsafe_allow_html=True)
        
        stats_data = []
        for city in env.cities:
            state = env.get_city_state(city)
            crisis_prob = bayesian.predict_crisis_probability(state)
            
            stats_data.append({
                'City': city.replace('_', ' '),
                'Occupancy': f"{state['occupancy_rate']*100:.1f}%",
                'Available Rooms': f"{state['available_rooms']:,}",
                'Total Capacity': f"{state['capacity']:,}",
                'Crisis Probability': f"{crisis_prob*100:.1f}%",
                'Matches Hosted': state['num_matches'],
                'Cluster': f"Cluster {state['cluster']}",
                'Status': state['stress_level'],
                'Messages Sent': state['messages_sent'],
                'Messages Received': state['messages_received']
            })
        
        df_stats = pd.DataFrame(stats_data)
        st.dataframe(df_stats, use_container_width=True, hide_index=True)
        
        export_col1, export_col2 = st.columns([3, 1])
        with export_col2:
            csv = df_stats.to_csv(index=False)
            st.download_button(
                label="📥 Export Report (CSV)",
                data=csv,
                file_name=f"fifa2026_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #64748b; padding: 2rem;'>
        <p style='font-size: 0.9rem; margin-bottom: 0.5rem;'>
            <strong>FIFA World Cup 2026 - Multi-Agent Crisis Management System</strong>
        </p>
        <p style='font-size: 0.8rem; margin: 0;'>
            Powered by Machine Learning • Bayesian Inference • Big Data Analytics • Agent Communication Networks
        </p>
        <p style='font-size: 0.75rem; margin-top: 0.5rem; color: #94a3b8;'>
            Real-time AI coordination with distributed agent architecture
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
