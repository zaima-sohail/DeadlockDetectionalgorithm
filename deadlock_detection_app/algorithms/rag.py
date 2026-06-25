import graphviz

def generate_rag(allocation, request, n_p, n_r, deadlocked_processes=None):
    """
    Generates a Resource Allocation Graph using Graphviz.
    """
    if deadlocked_processes is None:
        deadlocked_processes = []
        
    dot = graphviz.Digraph(comment='Resource Allocation Graph')
    dot.attr(rankdir='LR', size='8,5')
    dot.attr('node', fontname='Inter, sans-serif')
    
    # Process Nodes (Circles)
    for i in range(n_p):
        color = '#ef4444' if i in deadlocked_processes else '#6366f1'
        fontcolor = 'white'
        dot.node(f'P{i}', f'P{i}', shape='circle', style='filled', 
                 fillcolor=color, color=color, fontcolor=fontcolor)
        
    # Resource Nodes (Rectangles)
    for i in range(n_r):
        dot.node(f'R{i}', f'R{i}', shape='box', style='filled', 
                 fillcolor='#94a3b8', color='#64748b', fontcolor='white')
        
    # Edges: Allocation (R -> P)
    for p in range(n_p):
        for r in range(n_r):
            if allocation[p][r] > 0:
                # Allocation edge from Resource to Process
                # For simplicity, we draw one edge even if multiple units are allocated
                dot.edge(f'R{r}', f'P{p}', label=str(allocation[p][r]), color='#22c55e', fontcolor='#22c55e')
                
    # Edges: Request (P -> R)
    for p in range(n_p):
        for r in range(n_r):
            if request[p][r] > 0:
                # Request edge from Process to Resource
                dot.edge(f'P{p}', f'R{r}', label=str(request[p][r]), color='#ef4444', fontcolor='#ef4444', style='dashed')
                
    return dot
