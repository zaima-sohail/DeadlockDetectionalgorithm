import graphviz

def generate_rag(allocation, request, processes, resources, deadlocked_processes=None):
    """
    Generates a Resource Allocation Graph using Graphviz
    """
    if deadlocked_processes is None:
        deadlocked_processes = []
        
    dot = graphviz.Digraph(comment='Resource Allocation Graph')
    dot.attr(rankdir='LR', bgcolor='transparent')
    dot.attr('node', style='filled', fontcolor='black')
    
    # Add processes
    for p in range(processes):
        color = '#ff9999' if p in deadlocked_processes else '#lightblue'
        dot.node(f'P{p}', f'P{p}', shape='circle', fillcolor=color)
        
    # Add resources
    for r in range(resources):
        dot.node(f'R{r}', f'R{r}', shape='square', fillcolor='#lightgreen')
        
    # Add Allocation edges (Resource -> Process)
    for p in range(processes):
        for r in range(resources):
            if allocation[p][r] > 0:
                color = 'red' if p in deadlocked_processes else 'white'
                # For multiple instances, label the edge
                dot.edge(f'R{r}', f'P{p}', label=str(allocation[p][r]), color=color, fontcolor='white')
                
    # Add Request edges (Process -> Resource)
    if request is not None:
        for p in range(processes):
            for r in range(resources):
                if request[p][r] > 0:
                    color = 'red' if p in deadlocked_processes else 'white'
                    dot.edge(f'P{p}', f'R{r}', label=str(request[p][r]), style='dashed', color=color, fontcolor='white')
                    
    return dot
