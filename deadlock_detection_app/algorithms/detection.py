import numpy as np

def run_deadlock_detection(allocation, request, available):
    """
    Detailed Deadlock Detection Algorithm with full state capture for visualization.
    """
    n_p = allocation.shape[0]
    n_r = allocation.shape[1]
    
    work = available.copy()
    finish = np.zeros(n_p, dtype=bool)
    
    # Step 1: Initialize Finish
    # If allocation is 0 for all resources, finish[i] = True
    for i in range(n_p):
        if np.all(allocation[i] == 0):
            finish[i] = True
            
    steps = []
    
    # Initial state capture
    steps.append({
        'step_type': 'initial',
        'work': work.tolist(),
        'finish': finish.tolist(),
        'details': 'Initialization: Work set to Available. Processes with no allocation marked as Finish=True.',
        'explanation': 'We begin by setting the current Work vector to the system\'s Available resources.'
    })
    
    iteration = 1
    safe_sequence = []
    
    while True:
        found = False
        for i in range(n_p):
            if not finish[i]:
                # Record the check
                can_execute = np.all(request[i] <= work)
                
                step_data = {
                    'step_type': 'check',
                    'process': i,
                    'work_before': work.copy(),
                    'request': request[i].copy(),
                    'finish_before': finish.copy(),
                    'condition_passed': can_execute,
                    'iteration': iteration
                }
                
                if can_execute:
                    # Process can finish
                    old_work = work.copy()
                    work += allocation[i]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    
                    step_data.update({
                        'status': 'Executed',
                        'allocation_released': allocation[i].tolist(),
                        'work_after': work.tolist(),
                        'finish_after': finish.tolist(),
                        'finish': finish.tolist(),
                        'details': f'P{i} Request {request[i].tolist()} ≤ Work {old_work.tolist()}. Success!',
                        'explanation': f'Process P{i} can complete. Updated Work = {old_work.tolist()} + {allocation[i].tolist()} = {work.tolist()}.'
                    })
                    steps.append(step_data)
                    iteration += 1
                    break 
                else:
                    step_data.update({
                        'status': 'Waiting',
                        'details': f'P{i} Request {request[i].tolist()} > Work {work.tolist()}. Process must wait.',
                        'explanation': f'Process P{i} is requesting resources that are not currently available. It remains in the waiting state.',
                        'finish': finish.tolist()
                    })
                    steps.append(step_data)
                    iteration += 1
        
        if not found:
            break
            
    deadlocked = [i for i, f in enumerate(finish) if not f]
    is_deadlocked = len(deadlocked) > 0
    
    steps.append({
        'step_type': 'final',
        'is_deadlocked': is_deadlocked,
        'deadlocked_processes': deadlocked,
        'work': work.tolist(),
        'finish': finish.tolist(),
        'safe_sequence': safe_sequence,
        'details': 'Algorithm finished. ' + ('Deadlock detected!' if is_deadlocked else 'No deadlock detected.')
    })
    
    return is_deadlocked, deadlocked, steps
