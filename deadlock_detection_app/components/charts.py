import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def plot_resource_utilization(allocation, available, n_r):
    total_allocated = np.sum(allocation, axis=0)
    total_resources = total_allocated + available
    
    # Calculate percentages
    utilization = (total_allocated / total_resources) * 100
    
    df = pd.DataFrame({
        'Resource': [f'R{i}' for i in range(n_r)],
        'Allocated': total_allocated,
        'Free': available,
        'Utilization (%)': utilization
    })
    
    fig = px.bar(df, x='Resource', y=['Allocated', 'Free'], 
                 title="Resource Allocation Distribution",
                 color_discrete_map={'Allocated': '#3B82F6', 'Free': '#64748B'},
                 template="plotly_dark")
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter, sans-serif"
    )
    
    return fig

def plot_process_status(finish_array):
    completed = np.sum(finish_array)
    pending = len(finish_array) - completed
    
    fig = go.Figure(data=[go.Pie(
        labels=['Completed', 'Pending/Deadlocked'],
        values=[completed, pending],
        hole=.4,
        marker_colors=['#22C55E', '#F59E0B']
    )])
    
    fig.update_layout(
        title="Process Execution Progress",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig
