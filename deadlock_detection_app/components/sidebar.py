import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 class='gradient-text'>⚡ Deadlock Sim</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        selected = option_menu(
            menu_title=None,
            options=["Home", "Deadlock Detection", "Banker's Algorithm", "Resource Request", "RAG Viewer", "Theory & Comparison", "Analytics"],
            icons=["house", "search", "shield-check", "arrow-left-right", "diagram-3", "book", "graph-up"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#818cf8", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "rgba(99, 102, 241, 0.1)",
                    "color": "#94a3b8",
                },
                "nav-link-selected": {
                    "background-color": "rgba(99, 102, 241, 0.2)",
                    "color": "#6366f1",
                    "border-left": "4px solid #6366f1",
                    "font-weight": "600"
                },
            }
        )
        
        st.markdown("---")
        with st.expander("⚙️ Simulation Settings"):
            st.slider("Execution Speed", 0.1, 2.0, 1.0, key="sim_speed")
            st.checkbox("Auto-play", value=False, key="auto_play")
            
        st.markdown("---")
        st.caption("v1.0.0 | Senior OS Expert")
        
    return selected
