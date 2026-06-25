import pandas as pd
import numpy as np

def df_to_numpy(df):
    return df.to_numpy()

def numpy_to_df(arr, row_prefix="P", col_prefix="R"):
    rows, cols = arr.shape
    df = pd.DataFrame(
        arr,
        index=[f"{row_prefix}{i}" for i in range(rows)],
        columns=[f"{col_prefix}{i}" for i in range(cols)]
    )
    return df

def reset_simulation_state():
    if 'current_step_idx' in st.session_state:
        st.session_state.current_step_idx = 0
