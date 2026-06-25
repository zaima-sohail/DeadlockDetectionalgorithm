import streamlit as st
import pandas as pd
import numpy as np
import time

# UI & Layout Imports
from components.sidebar import render_sidebar
from components.matrix_input import render_matrix_inputs, get_presets
from components.visualization import render_dry_run, to_latex_matrix
from components.charts import plot_resource_utilization, plot_process_status
from components.animations import show_hero_animation, show_success_animation, show_error_animation

# Logic Imports
from algorithms.detection import run_deadlock_detection
from algorithms.banker import is_safe_state, calculate_need
from algorithms.rag import generate_rag
from utils.validators import validate_matrices, validate_bankers_matrices
from utils.helpers import df_to_numpy

# Page Config
st.set_page_config(
    page_title="Deadlock Expert Simulator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
css_path = 'deadlock_detection_app/assets/styles.css'
try:
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    try:
        with open('assets/styles.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass

# Main Navigation
selected = render_sidebar()

if selected == "Home":
    st.markdown("<h1 class='gradient-text'>Operating Systems: Deadlock Expert</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("""
        <div class='glass-card'>
        <h3>Welcome, Students! 🎓</h3>
        <p>This simulator provides a <b>Deep Dive</b> into how Operating Systems manage resource contention and handle deadlocks.</p>
        
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px;'>
            <div class='info-box'><b>Detection</b><br>Analyze blocked states</div>
            <div class='info-box'><b>Avoidance</b><br>Banker's Algorithm logic</div>
            <div class='info-box'><b>Visualization</b><br>Real-time RAG tracking</div>
            <div class='info-box'><b>Control</b><br>Step-by-step execution</div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        show_hero_animation()
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 💡 Getting Started")
    c1, c2, c3 = st.columns(3)
    c1.info("🔍 **Deadlock Detection**: Visualize resource requests and find cycles.")
    c2.info("🛡️ **Banker's Algorithm**: Ensure system safety during allocation.")
    c3.info("📈 **RAG Viewer**: Explore dependency graphs interactively.")

elif selected == "Resource Request":
    st.markdown("<h1 class='gradient-text'>🔧 Resource Request Simulation</h1>", unsafe_allow_html=True)
    
    # Configuration Section (reuse matrix input)
    col_input, col_viz, col_console = st.columns([1.2, 2.5, 2.0])
    
    with col_input:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Configuration")
        c1, c2 = st.columns(2)
        n_p = c1.number_input("Processes", 1, 10, 5, key="req_np")
        n_r = c2.number_input("Resources", 1, 10, 3, key="req_nr")
        
        df_alloc, df_req, df_avail = render_matrix_inputs(n_p, n_r, "resource_request")
        st.markdown("</div>", unsafe_allow_html=True)
    
    alloc = df_to_numpy(df_alloc)
    req = df_to_numpy(df_req)
    avail = df_to_numpy(df_avail).flatten()
    
    is_valid, msg = validate_matrices(alloc, req, avail, n_p, n_r)
    
    if not is_valid:
        st.error(msg)
    else:
        with col_viz:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 📊 Live System Visualization")
            if st.button("🚀 Initialize Request Simulation", width='stretch', key="btn_req_run"):
                is_deadlocked, deadlocked, steps = run_deadlock_detection(alloc, req, avail)
                st.session_state.request_steps = steps
                st.session_state.current_step_idx = 0
                st.session_state.is_deadlocked = is_deadlocked
                st.session_state.deadlocked = deadlocked
            
            tab_rag, tab_charts, tab_matrices = st.tabs(["Graph", "Stats", "Matrices"])
            with tab_rag:
                dead_p = st.session_state.get('deadlocked', []) if st.session_state.get('is_deadlocked') else []
                dot = generate_rag(alloc, req, n_p, n_r, dead_p)
                st.graphviz_chart(dot, width='stretch')
            with tab_charts:
                st.plotly_chart(plot_resource_utilization(alloc, avail, n_r), width='stretch')
            with tab_matrices:
                st.markdown("### 🧮 System Matrices")
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.latex(to_latex_matrix(alloc))
                with m2:
                    st.latex(to_latex_matrix(req))
                with m3:
                    st.latex(to_latex_matrix([avail]))
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_console:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            if 'request_steps' in st.session_state:
                render_dry_run(st.session_state.request_steps, "detection")
            else:
                st.info("Awaiting request simulation start…")
            st.markdown("</div>", unsafe_allow_html=True)
elif selected == "RAG Viewer":
    st.markdown("<h1 class='gradient-text'>📈 Resource Allocation Graph Viewer</h1>", unsafe_allow_html=True)
    
    # Configuration (reuse matrix inputs)
    col_input, col_viz = st.columns([1.2, 2.5])
    
    with col_input:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Configuration")
        c1, c2 = st.columns(2)
        n_p = c1.number_input("Processes", 1, 10, 5, key="rag_np")
        n_r = c2.number_input("Resources", 1, 10, 3, key="rag_nr")
        df_alloc, df_req, df_avail = render_matrix_inputs(n_p, n_r, "rag_viewer")
        st.markdown("</div>", unsafe_allow_html=True)
    
    alloc = df_to_numpy(df_alloc)
    req = df_to_numpy(df_req)
    avail = df_to_numpy(df_avail).flatten()
    
    is_valid, msg = validate_matrices(alloc, req, avail, n_p, n_r)
    if not is_valid:
        st.error(msg)
    else:
        with col_viz:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 📊 Resource Allocation Graph")
            dot = generate_rag(alloc, req, n_p, n_r, [])
            st.graphviz_chart(dot, width='stretch')
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Continue to Deadlock Detection block
    
elif selected == "Deadlock Detection":
    
    col_input, col_viz, col_console = st.columns([1.2, 2.5, 2.0])
    
    with col_input:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Configuration")
        c1, c2 = st.columns(2)
        n_p = c1.number_input("Processes", 1, 10, 5, key="det_np")
        n_r = c2.number_input("Resources", 1, 10, 3, key="det_nr")
        
        presets = get_presets()
        preset_choice = st.selectbox("Load Preset", ["Custom"] + list(presets.keys()), key="det_preset")
        
        df_alloc, df_req, df_avail = render_matrix_inputs(n_p, n_r, "detection")
        st.markdown("</div>", unsafe_allow_html=True)
        
    alloc = df_to_numpy(df_alloc)
    req = df_to_numpy(df_req)
    avail = df_to_numpy(df_avail).flatten()
    
    is_valid, msg = validate_matrices(alloc, req, avail, n_p, n_r)
    
    if not is_valid:
        with col_viz:
            st.error(msg)
    else:
        with col_viz:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 📊 Active Visualization")
            if st.button("🚀 Initialize Detection", width='stretch', key="btn_det_run"):
                is_deadlocked, deadlocked, steps = run_deadlock_detection(alloc, req, avail)
                st.session_state.detection_steps = steps
                st.session_state.current_step_idx = 0
                st.session_state.is_deadlocked = is_deadlocked
                st.session_state.deadlocked = deadlocked
                st.success("🟢 Simulation initialized. Use the controls to step through.")
            
            tab_rag, tab_charts, tab_matrices = st.tabs(["Graph", "Stats", "Matrices"])
            with tab_rag:
                dead_p = st.session_state.get('deadlocked', []) if st.session_state.get('is_deadlocked') else []
                dot = generate_rag(alloc, req, n_p, n_r, dead_p)
                st.graphviz_chart(dot, width='stretch')
            with tab_charts:
                st.plotly_chart(plot_resource_utilization(alloc, avail, n_r), width='stretch')
            with tab_matrices:
                st.markdown("### 🧮 System State Matrices")
                st.caption("Current state represented in professional textbook format.")
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.markdown("<div style='text-align: center; color: var(--text-muted);'><b>Allocation</b></div>", unsafe_allow_html=True)
                    st.latex(to_latex_matrix(alloc))
                with m2:
                    st.markdown("<div style='text-align: center; color: var(--text-muted);'><b>Request</b></div>", unsafe_allow_html=True)
                    st.latex(to_latex_matrix(req))
                with m3:
                    st.markdown("<div style='text-align: center; color: var(--text-muted);'><b>Available</b></div>", unsafe_allow_html=True)
                    st.latex(to_latex_matrix([avail]))
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_console:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            if 'detection_steps' in st.session_state:
                render_dry_run(st.session_state.detection_steps, "detection")
            else:
                st.info("Awaiting simulation start...")
            st.markdown("</div>", unsafe_allow_html=True)

elif selected == "Banker's Algorithm":
    st.markdown("<h1 class='gradient-text'>🛡️ Banker's Safety Algorithm</h1>", unsafe_allow_html=True)
    
    col_input, col_viz, col_console = st.columns([1.2, 2.5, 2.0])
    
    with col_input:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Configuration")
        c1, c2 = st.columns(2)
        n_p = c1.number_input("Processes", 1, 10, 5, key="bank_np")
        n_r = c2.number_input("Resources", 1, 10, 3, key="bank_nr")
        
        df_alloc, df_max, df_avail = render_matrix_inputs(n_p, n_r, "banker")
        st.markdown("</div>", unsafe_allow_html=True)
        
    alloc = df_to_numpy(df_alloc)
    max_m = df_to_numpy(df_max)
    avail = df_to_numpy(df_avail).flatten()
    
    is_valid, msg = validate_bankers_matrices(alloc, max_m, avail, n_p, n_r)
    
    if not is_valid:
        with col_viz:
            st.error(msg)
    else:
        with col_viz:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 📉 Analysis Dashboard")
            if st.button("🛡️ Initialize Safety Check", width='stretch', key="btn_bank_run"):
                is_safe, sequence, steps, need = is_safe_state(alloc, max_m, avail)
                st.session_state.banker_steps = steps
                st.session_state.current_step_idx = 0
                st.session_state.is_safe = is_safe
                
            if 'banker_steps' in st.session_state:
                tab_rag, tab_matrices = st.tabs(["Analysis Dashboard", "System Matrices"])
                with tab_rag:
                    last_step = st.session_state.banker_steps[st.session_state.current_step_idx]
                    st.plotly_chart(plot_process_status(last_step['finish']), width='stretch')
                    st.plotly_chart(plot_resource_utilization(alloc, avail, n_r), width='stretch')
                with tab_matrices:
                    st.markdown("### 🧮 System State Matrices")
                    st.caption("Current state represented in professional textbook format.")
                    need_m = max_m - alloc
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.markdown("<div style='text-align: center; color: var(--text-muted);'><b>Allocation</b></div>", unsafe_allow_html=True)
                        st.latex(to_latex_matrix(alloc))
                    with m2:
                        st.markdown("<div style='text-align: center; color: var(--text-muted);'><b>Need</b></div>", unsafe_allow_html=True)
                        st.latex(to_latex_matrix(need_m))
                    with m3:
                        st.markdown("<div style='text-align: center; color: var(--text-muted);'><b>Available</b></div>", unsafe_allow_html=True)
                        st.latex(to_latex_matrix([avail]))
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_console:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            if 'banker_steps' in st.session_state:
                render_dry_run(st.session_state.banker_steps, "banker")
            else:
                st.info("Awaiting safety check initialization...")
            st.markdown("</div>", unsafe_allow_html=True)

elif selected == "Theory & Comparison":
    st.markdown("<h1 class='gradient-text'>📖 Learning Center</h1>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Deadlock Basics", "Coffman Conditions", "Detection vs Avoidance", "Interview Prep"])
    
    with tabs[0]:
        st.markdown("""
        ### What is a Deadlock?
        A state where a set of processes are blocked because each process is holding a resource and waiting for another resource held by some other process.
        
        **Example:**
        Process A holds Resource 1 and wants Resource 2.
        Process B holds Resource 2 and wants Resource 1.
        """)
        
    with tabs[1]:
        st.markdown("""
        ### The Four Must-Have Conditions:
        1. **Mutual Exclusion:** Resources cannot be shared.
        2. **Hold and Wait:** Process holds one and waits for more.
        3. **No Preemption:** Resources only released voluntarily.
        4. **Circular Wait:** A chain of waiting exists.
        """)

elif selected == "Analytics":
    st.markdown("<h1 class='gradient-text'>📈 System Analytics</h1>", unsafe_allow_html=True)
    st.info("Run a simulation in the Detection or Banker's tabs to see aggregated analytics here.")
    # Add more complex plotly charts here if needed.
