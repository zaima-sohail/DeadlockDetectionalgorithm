import numpy as np

def calculate_need(max_matrix, allocation):
    return max_matrix - allocation

def is_safe_state(allocation, max_matrix, available):
    """
    Banker's Algorithm: Safety Algorithm with full step capture.
    """
    n_p = allocation.shape[0]
    n_r = allocation.shape[1]
    
    need = calculate_need(max_matrix, allocation)
    work = available.copy()
    finish = np.zeros(n_p, dtype=bool)
    
    safe_sequence = []
    steps = []
    
    steps.append({
        'step_type': 'initial',
        'work': work.tolist(),
        'finish': finish.tolist(),
        'need': need.tolist(),
        'details': 'Initialization: Work set to Available, Need calculated.',
        'explanation': 'In the Banker\'s algorithm, we calculate Need = Max - Allocation to see what each process might require.'
    })
    
    iteration = 1
    while len(safe_sequence) < n_p:
        found = False
        for i in range(n_p):
            if not finish[i]:
                can_execute = np.all(need[i] <= work)
                
                step_data = {
                    'step_type': 'check',
                    'process': i,
                    'work_before': work.copy(),
                    'need_val': need[i].copy(),
                    'finish_before': finish.copy(),
                    'condition_passed': can_execute,
                    'iteration': iteration
                }
                
                if can_execute:
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
                        'details': f'P{i} Need {need[i].tolist()} ≤ Work {old_work.tolist()}. Safe!',
                        'explanation': f'Process P{i} can complete. Updated Work = {old_work.tolist()} + {allocation[i].tolist()} = {work.tolist()}.'
                    })
                    steps.append(step_data)
                    iteration += 1
                    break
                else:
                    step_data.update({
                        'status': 'Waiting',
                        'details': f'P{i} Need {need[i].tolist()} > Work {work.tolist()}. Unsafe to grant now.',
                        'explanation': f'Process P{i} cannot be guaranteed to finish right now. We wait for other processes to release resources.',
                        'finish': finish.tolist()
                    })
                    steps.append(step_data)
                    iteration += 1
                    
        if not found:
            break
            
    is_safe = len(safe_sequence) == n_p
    
    steps.append({
        'step_type': 'final',
        'is_safe': is_safe,
        'safe_sequence': safe_sequence,
        'work': work.tolist(),
        'finish': finish.tolist(),
        'details': 'Safety check complete. ' + ('System is in a SAFE state.' if is_safe else 'System is in an UNSAFE state.')
    })
    
    return is_safe, safe_sequence, steps, need

def resource_request(process_id, request_vector, allocation, max_matrix, available):
    """
    Banker's Algorithm: Resource Request algorithm with full step capture.

    process_id: int (P_i)
    request_vector: 1D array-like (R_j request for P_i)
    allocation: 2D array-like (n_p x n_r)
    max_matrix: 2D array-like (n_p x n_r)
    available: 1D array-like (n_r)

    Returns:
      (granted: bool, message: str, steps: list[dict])
    """
    request_vector = np.array(request_vector)
    allocation = np.array(allocation)
    max_matrix = np.array(max_matrix)
    available = np.array(available)

    need = calculate_need(max_matrix, allocation)

    steps = []
    iteration = 1

    steps.append({
        'step_type': 'request_initial',
        'iteration': iteration,
        'process': int(process_id),
        'request': request_vector.tolist(),
        'need_for_process_before': need[int(process_id)].tolist(),
        'available_before': available.tolist(),
        'finish_note': 'Banker pre-checks: (1) Request ≤ Need (2) Request ≤ Available',
        'details': 'Starting resource request handling: compute Need = Max - Allocation and compare request against it and Available.',
        'explanation': 'Banker’s request algorithm first ensures the request is within the process’s declared maximum need, then ensures the system currently has the resources.'
    })

    iteration += 1

    # 1) Check Request <= Need
    req_exceeds_need = np.any(request_vector > need[int(process_id)])
    steps.append({
        'step_type': 'check_need',
        'iteration': iteration,
        'process': int(process_id),
        'request': request_vector.tolist(),
        'need_for_process': need[int(process_id)].tolist(),
        'condition_passed': not req_exceeds_need,
        'status': 'Waiting' if req_exceeds_need else 'Eligible',
        'details': (
            f'Check: Request[{int(process_id)}] ≤ Need[{int(process_id)}]. '
            + ('Condition FAILED (request exceeds declared need).' if req_exceeds_need else 'Condition PASSED.')
        ),
        'explanation': 'If the request exceeds what the process can ever need (its Max claim), the request must be rejected.'
    })

    if req_exceeds_need:
        return False, "Error: Process requested more than its declared Max Need.", steps

    iteration += 1

    # 2) Check Request <= Available
    req_exceeds_available = np.any(request_vector > available)
    steps.append({
        'step_type': 'check_available',
        'iteration': iteration,
        'process': int(process_id),
        'request': request_vector.tolist(),
        'available_before': available.tolist(),
        'condition_passed': not req_exceeds_available,
        'status': 'Waiting' if req_exceeds_available else 'Eligible',
        'details': (
            f'Check: Request[{int(process_id)}] ≤ Available. '
            + ('Condition FAILED (resources unavailable).' if req_exceeds_available else 'Condition PASSED.')
        ),
        'explanation': 'If the system does not currently have enough resources available, the request cannot be granted right now.'
    })

    if req_exceeds_available:
        return False, f"Error: Resources unavailable. Process P{int(process_id)} must wait.", steps

    # 3) Pretend allocation is granted and run safety check
    new_available = available - request_vector
    new_allocation = allocation.copy()
    new_allocation[int(process_id)] += request_vector
    new_need = calculate_need(max_matrix, new_allocation)

    iteration += 1
    steps.append({
        'step_type': 'pretend_grant',
        'iteration': iteration,
        'process': int(process_id),
        'request': request_vector.tolist(),
        'available_before': available.tolist(),
        'available_after': new_available.tolist(),
        'allocation_before': allocation[int(process_id)].tolist(),
        'allocation_after': new_allocation[int(process_id)].tolist(),
        'need_for_process_before': need[int(process_id)].tolist(),
        'need_for_process_after': new_need[int(process_id)].tolist(),
        'details': 'Pretending the request is granted: Available and Allocation are updated, then Need recomputed.',
        'explanation': 'Banker’s algorithm grants provisionally and then checks if the resulting state is safe.'
    })

    is_safe, safe_sequence, safety_steps, _ = is_safe_state(new_allocation, max_matrix, new_available)

    # Merge safety steps while keeping trace continuity
    # (Safety algorithm already includes an 'initial' and 'final' step.)
    steps.extend(safety_steps)

    # 4) Final decision step
    steps.append({
        'step_type': 'request_final',
        'iteration': iteration + len(safety_steps) + 1,
        'process': int(process_id),
        'granted': bool(is_safe),
        'safe_sequence': [int(x) for x in safe_sequence],
        'available_after': new_available.tolist(),
        'details': 'Request handling complete. ' + ('Request GRANTED (state is SAFE).' if is_safe else 'Request DENIED (state would be UNSAFE).'),
        'explanation': 'If and only if the provisional grant results in a safe state, the request can be permanently granted.'
    })

    if is_safe:
        return True, "Request Granted! System remains in a safe state.", steps
    return False, "Request Denied! Granting this would leave the system in an unsafe state.", steps

