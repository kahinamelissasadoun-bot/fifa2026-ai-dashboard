"""
FIFA 2026 Multi-Agent Crisis Management System
Interactive Web Dashboard with Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from sklearn.tree import DecisionTreeClassifier

# ============================================================================
# CONFIGURATION STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="FIFA 2026 AI System",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CLASSES DU SYSTÈME (COPIE DE TON CODE)
# ============================================================================

class EnvironmentHybrid:
    """Environment class - copie simplifié de ton code"""
    def __init__(self, cities_data):
        self.cities = list(cities_data.keys())
        self.dynamic_state = {}
        
        for city, data in cities_data.items():
            self.dynamic_state[city] = {
                'occupancy_rate': data['occupancy'],
                'crisis_level': 0.0,
                'available_rooms': data['capacity'],
                'stress_level': 'BAS',
                'resources_received': 0,
                'resources_given': 0,
                'cluster': data['cluster'],
                'popularity_rank': data['popularity']
            }
    
    def get_city_state(self, city):
        occ = self.dynamic_state[city]['occupancy_rate']
        capacity = self.dynamic_state[city]['available_rooms']
        
        # Calculer stress
        if occ >= 0.85:
            stress = 'CRITIQUE'
            crisis = 0.9
        elif occ >= 0.70:
            stress = 'ELEVE'
            crisis = 0.7
        elif occ >= 0.50:
            stress = 'MOYEN'
            crisis = 0.4
        else:
            stress = 'BAS'
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
            'resources_given': self.dynamic_state[city]['resources_given']
        }

class BayesianCrisisPredictor:
    """Prédicteur Bayésien simplifié"""
    def __init__(self):
        pass
    
    def predict_crisis_probability(self, city_state):
        occ = city_state['occupancy_rate']
        cluster_score = 0.60 if city_state['cluster'] == 0 else 0.40
        
        crisis_prob = 0.60 * occ + 0.20 * 0.55 + 0.20 * cluster_score
        return np.clip(crisis_prob, 0.0, 1.0)
    
    def classify_risk_ml(self, city_state):
        occ = city_state['occupancy_rate']
        if occ >= 0.75:
            return 'HIGH_RISK'
        elif occ >= 0.50:
            return 'MEDIUM_RISK'
        else:
            return 'LOW_RISK'

class AgentCoordinator:
    """Coordinateur simplifié"""
    def __init__(self):
        self.interventions = 0
        self.crises_resolved = 0
        self.transfers_log = []
    
    def detect_and_coordinate(self, env, bayesian):
        crises = []
        helpers = []
        
        for city in env.cities:
            state = env.get_city_state(city)
            crisis_prob = bayesian.predict_crisis_probability(state)
            
            if crisis_prob >= 0.68 or state['occupancy_rate'] >= 0.78:
                crises.append(city)
            elif crisis_prob < 0.52 and state['occupancy_rate'] < 0.60:
                helpers.append(city)
        
        # Exécuter transferts
        if len(crises) > 0 and len(helpers) > 0:
            for crisis_city in crises[:2]:  # Max 2 crises
                if helpers:
                    helper = helpers[0]
                    self.transfer_resources(env, helper, crisis_city, 0.15)
                    self.transfers_log.append(f"{helper} → {crisis_city}")
                    self.interventions += 1
            
            self.crises_resolved = len(crises)
        
        return len(crises), len(helpers)
    
    def transfer_resources(self, env, from_city, to_city, reduction):
        current_occ = env.dynamic_state[to_city]['occupancy_rate']
        new_occ = max(0.30, current_occ - reduction)
        env.dynamic_state[to_city]['occupancy_rate'] = new_occ
        
        capacity = 6000000  # Capacité moyenne
        resources = int(capacity * reduction)
        env.dynamic_state[to_city]['resources_received'] += resources
        env.dynamic_state[from_city]['resources_given'] += resources

def calculate_system_score(env):
    """Calcul du score système"""
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
        
        crisis_score = 10 if state['crisis_level'] < 0.30 else 5
        total += occ_score + crisis_score
    
    return int((total / (22 * len(env.cities))) * 100)

# ============================================================================
# INTERFACE STREAMLIT
# ============================================================================

def main():
    # Header
    st.markdown('<h1 class="main-header">⚽ FIFA 2026 Multi-Agent Crisis Management</h1>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("🎛️ Control Panel")
    st.sidebar.markdown("### Adjust City Occupancy Rates")
    
    # Sliders
    occ_la = st.sidebar.slider("🏙️ Los Angeles", 0.30, 0.95, 0.60, 0.05)
    occ_mexico = st.sidebar.slider("🏙️ Mexico City", 0.30, 0.95, 0.47, 0.05)
    occ_ny = st.sidebar.slider("🏙️ New York", 0.30, 0.95, 0.48, 0.05)
    occ_toronto = st.sidebar.slider("🏙️ Toronto", 0.30, 0.95, 0.84, 0.05)
    
    st.sidebar.markdown("---")
    use_coordinator = st.sidebar.checkbox("✅ Use Coordinator Agent", value=True)
    
    st.sidebar.markdown("---")
    
    # Scénarios prédéfinis
    st.sidebar.markdown("### 🎯 Quick Scenarios")
    col1, col2 = st.sidebar.columns(2)
    
    if col1.button("🟢 Normal", use_container_width=True):
        occ_la, occ_mexico, occ_ny, occ_toronto = 0.55, 0.50, 0.48, 0.60
        st.rerun()
    
    if col2.button("🔴 Crisis", use_container_width=True):
        occ_la, occ_mexico, occ_ny, occ_toronto = 0.88, 0.85, 0.42, 0.91
        st.rerun()
    
    # Bouton principal
    run_simulation = st.sidebar.button("🚀 RUN SIMULATION", 
                                       type="primary", 
                                       use_container_width=True)
    
    # ========================================================================
    # SIMULATION
    # ========================================================================
    
    if run_simulation or 'first_run' not in st.session_state:
        st.session_state.first_run = True
        
        with st.spinner("⏳ Running simulation..."):
            # Initialiser environment
            cities_data = {
                'Los_Angeles': {'occupancy': occ_la, 'capacity': 6659579, 'cluster': 1, 'popularity': 2},
                'Mexico_City': {'occupancy': occ_mexico, 'capacity': 3736279, 'cluster': 0, 'popularity': 3},
                'New_York': {'occupancy': occ_ny, 'capacity': 7240856, 'cluster': 1, 'popularity': 1},
                'Toronto': {'occupancy': occ_toronto, 'capacity': 2598127, 'cluster': 0, 'popularity': 4}
            }
            
            env = EnvironmentHybrid(cities_data)
            bayesian = BayesianCrisisPredictor()
            coordinator = AgentCoordinator()
            
            # Score initial
            score_initial = calculate_system_score(env)
            
            # Coordination (si activée)
            crises_detected = 0
            helpers_available = 0
            
            if use_coordinator:
                crises_detected, helpers_available = coordinator.detect_and_coordinate(env, bayesian)
            
            # Score final
            score_final = calculate_system_score(env)
            
            # Stocker résultats
            st.session_state.results = {
                'env': env,
                'coordinator': coordinator,
                'bayesian': bayesian,
                'score_initial': score_initial,
                'score_final': score_final,
                'crises_detected': crises_detected,
                'helpers_available': helpers_available,
                'use_coordinator': use_coordinator
            }
    
    # ========================================================================
    # AFFICHAGE RÉSULTATS
    # ========================================================================
    
    if 'results' in st.session_state:
        results = st.session_state.results
        env = results['env']
        coordinator = results['coordinator']
        
        # Métriques
        st.markdown("## 📊 Simulation Results")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            delta = results['score_final'] - results['score_initial']
            st.metric("Final Score", 
                     f"{results['score_final']}/100", 
                     f"+{delta}" if delta >= 0 else f"{delta}")
        
        with col2:
            st.metric("Crises Detected", 
                     results['crises_detected'],
                     "🔴" if results['crises_detected'] > 0 else "🟢")
        
        with col3:
            st.metric("Helpers Available", 
                     results['helpers_available'],
                     "✅" if results['helpers_available'] > 0 else "⚠️")
        
        with col4:
            if results['use_coordinator']:
                st.metric("Crises Resolved", 
                         coordinator.crises_resolved,
                         f"{coordinator.interventions} transfers")
            else:
                st.metric("Coordinator", "OFF", "⚠️")
        
        st.markdown("---")
        
        # Graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏙️ City Occupancy Rates")
            
            cities = []
            occupancies = []
            colors_list = []
            
            for city in env.cities:
                state = env.get_city_state(city)
                cities.append(city.replace('_', ' '))
                occupancies.append(state['occupancy_rate'] * 100)
                
                if state['occupancy_rate'] >= 0.78:
                    colors_list.append('#ff6b6b')
                elif state['occupancy_rate'] >= 0.60:
                    colors_list.append('#ffa726')
                else:
                    colors_list.append('#51cf66')
            
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            bars = ax1.bar(cities, occupancies, color=colors_list, alpha=0.8, edgecolor='black', linewidth=2)
            
            ax1.axhline(y=78, color='red', linestyle='--', linewidth=2, label='Crisis (78%)', alpha=0.7)
            ax1.axhline(y=60, color='orange', linestyle='--', linewidth=1.5, label='Warning (60%)', alpha=0.7)
            
            ax1.set_ylabel('Occupancy Rate (%)', fontsize=13, fontweight='bold')
            ax1.set_title('Hotel Occupancy by City', fontsize=14, fontweight='bold')
            ax1.set_ylim(0, 105)
            ax1.legend(fontsize=11)
            ax1.grid(axis='y', alpha=0.3)
            
            for bar, occ in zip(bars, occupancies):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
                        f'{occ:.1f}%', ha='center', va='bottom', 
                        fontsize=12, fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig1)
        
        with col2:
            st.markdown("### 📈 System Performance")
            
            # Simulation de score evolution (2 cycles)
            scores = [results['score_initial'], results['score_final']]
            cycles = [1, 2]
            
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.plot(cycles, scores, marker='o', linewidth=4, markersize=12, 
                    color='#4CAF50', label='System Score')
            ax2.fill_between(cycles, scores, alpha=0.3, color='#4CAF50')
            
            ax2.set_xlabel('Cycle', fontsize=13, fontweight='bold')
            ax2.set_ylabel('Score (/100)', fontsize=13, fontweight='bold')
            ax2.set_title('Score Evolution', fontsize=14, fontweight='bold')
            ax2.set_ylim(0, 105)
            ax2.grid(True, alpha=0.3)
            ax2.legend(fontsize=11)
            
            # Annotation
            improvement = results['score_final'] - results['score_initial']
            ax2.annotate(f'{"+" if improvement >= 0 else ""}{improvement} pts',
                        xy=(2, results['score_final']),
                        xytext=(1.5, results['score_final'] - 10),
                        fontsize=12, fontweight='bold',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                        arrowprops=dict(arrowstyle='->', lw=2))
            
            plt.tight_layout()
            st.pyplot(fig2)
        
        st.markdown("---")
        
        # Tableau détaillé
        st.markdown("### 🏙️ Detailed City Status")
        
        data_table = []
        for city in env.cities:
            state = env.get_city_state(city)
            
            status = "🔴 CRISIS" if state['occupancy_rate'] >= 0.78 else \
                     "🟡 WARNING" if state['occupancy_rate'] >= 0.60 else "🟢 STABLE"
            
            data_table.append({
                'City': city.replace('_', ' '),
                'Status': status,
                'Occupancy': f"{state['occupancy_rate']*100:.1f}%",
                'Available Rooms': f"{state['available_rooms']:,}",
                'Stress Level': state['stress_level'],
                'Rooms Received': f"{state['resources_received']:,}" if state['resources_received'] > 0 else "---",
                'Rooms Given': f"{state['resources_given']:,}" if state['resources_given'] > 0 else "---"
            })
        
        df = pd.DataFrame(data_table)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Transferts
        if results['use_coordinator'] and coordinator.transfers_log:
            st.markdown("### 🔄 Resource Transfers")
            for i, transfer in enumerate(coordinator.transfers_log, 1):
                st.success(f"**Transfer {i}:** {transfer}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p><b>FIFA 2026 Multi-Agent Crisis Management System</b></p>
        <p>Powered by Machine Learning, Bayesian Inference & Big Data</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
