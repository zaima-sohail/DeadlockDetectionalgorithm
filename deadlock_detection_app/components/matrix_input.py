import streamlit as st
import pandas as pd
import numpy as np

def render_matrix_inputs(num_p, num_r, key_prefix):
    """
    Renders editable matrices for Allocation and Request/Max.
    """
    st.markdown(f"### 📊 Configuration: {key_prefix.replace('_', ' ').title()}")
    
    st.markdown("**Allocation Matrix**")
    st.caption("Resources currently held by each process.")
    default_alloc = pd.DataFrame(
        np.zeros((num_p, num_r), dtype=int),
        columns=[f"R{i}" for i in range(num_r)],
        index=[f"P{i}" for i in range(num_p)]
    )
    df_alloc = st.data_editor(default_alloc, use_container_width=True, key=f"{key_prefix}_alloc")
    
    st.markdown("---")
    if "banker" in key_prefix.lower():
        label = "Max Matrix"
        caption = "Maximum resources each process may claim."
    else:
        label = "Request Matrix"
        caption = "Additional resources each process is currently requesting."
        
    st.markdown(f"**{label}**")
    st.caption(caption)
    default_req = pd.DataFrame(
        np.zeros((num_p, num_r), dtype=int),
        columns=[f"R{i}" for i in range(num_r)],
        index=[f"P{i}" for i in range(num_p)]
    )
    df_req = st.data_editor(default_req, use_container_width=True, key=f"{key_prefix}_req")
    
    st.markdown("---")
    st.markdown("**Available Vector**")
    st.caption("Resources currently free in the system.")
    default_avail = pd.DataFrame(
        np.zeros((1, num_r), dtype=int),
        columns=[f"R{i}" for i in range(num_r)],
        index=["Units"]
    )
    df_avail = st.data_editor(default_avail, use_container_width=True, key=f"{key_prefix}_avail")
    
    return df_alloc, df_req, df_avail

def get_presets():
    return {
        "Safe Scenario (Detection)": {
            "n_p": 5, "n_r": 3,
            "alloc": [[0,1,0],[2,0,0],[3,0,3],[2,1,1],[0,0,2]],
            "req": [[0,0,0],[2,0,2],[0,0,0],[1,0,0],[0,0,2]],
            "avail": [0,0,0]
        },
        "Deadlock Detected": {
            "n_p": 5, "n_r": 3,
            "alloc": [[0,1,0],[2,0,0],[3,0,3],[2,1,1],[0,0,2]],
            "req": [[0,0,0],[2,0,2],[0,0,1],[1,0,0],[0,0,2]],
            "avail": [0,0,0]
        }
    }
