import numpy as np

def validate_matrices(alloc, req, avail, n_p, n_r):
    """
    Validates the input matrices for consistency.
    """
    if np.any(alloc < 0) or np.any(req < 0) or np.any(avail < 0):
        return False, "Negative values are not allowed in resource matrices."
    
    if alloc.shape != (n_p, n_r):
        return False, f"Allocation matrix must be {n_p}x{n_r}."
        
    if req.shape != (n_p, n_r):
        return False, f"Request/Max matrix must be {n_p}x{n_r}."
        
    if len(avail) != n_r:
        return False, f"Available vector must have {n_r} elements."
        
    return True, ""

def validate_bankers_matrices(alloc, max_m, avail, n_p, n_r):
    """
    Validates input for Banker's Algorithm.
    """
    is_valid, msg = validate_matrices(alloc, max_m, avail, n_p, n_r)
    if not is_valid:
        return False, msg
        
    # Check if Allocation > Max
    if np.any(alloc > max_m):
        return False, "Error: Allocation cannot be greater than Maximum claim for any process."
        
    return True, ""
