import numpy as np
import sys
import time

# ANSI Color Codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DeadlockSimulator:
    """
    A Deadlock Detection Algorithm Simulator designed for educational purposes.
    Implements the standard OS algorithm with a detailed dry-run explanation.
    """

    def __init__(self, n_processes, n_resources, allocation, request, available):
        self.n_processes = n_processes
        self.n_resources = n_resources
        self.allocation = np.array(allocation)
        self.request = np.array(request)
        self.available = np.array(available)
        
        # Algorithm variables
        self.work = self.available.copy()
        self.finish = np.zeros(n_processes, dtype=bool)
        self.safe_sequence = []
        self.deadlocked_processes = []
        
        self.validate_inputs()

    def validate_inputs(self):
        """Validates the dimensions and values of the input matrices."""
        if self.allocation.shape != (self.n_processes, self.n_resources):
            raise ValueError(f"Allocation matrix shape {self.allocation.shape} does not match {self.n_processes}x{self.n_resources}")
        if self.request.shape != (self.n_processes, self.n_resources):
            raise ValueError(f"Request matrix shape {self.request.shape} does not match {self.n_processes}x{self.n_resources}")
        if self.available.shape != (self.n_resources,):
            raise ValueError(f"Available vector shape {self.available.shape} does not match {self.n_resources}")
        
        if np.any(self.allocation < 0) or np.any(self.request < 0) or np.any(self.available < 0):
            raise ValueError("All resource values must be non-negative.")

    def explain_initialization(self):
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*50}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}         DEADLOCK DETECTION ALGORITHM DRY RUN{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*50}{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}--- INITIAL STATE ---{Colors.ENDC}")
        print(f"{Colors.CYAN}Available (Work) = {self.work.tolist()}{Colors.ENDC}")
        
        print("\nFinish Array Initialization:")
        # According to standard algorithm, if Allocation[i] is 0, Finish[i] can be true
        # but usually, we start all False and check Request.
        # Expert Note: In deadlock detection, if a process has NO allocation, 
        # it is essentially not holding anything that could cause a deadlock.
        for i in range(self.n_processes):
            if np.all(self.allocation[i] == 0):
                self.finish[i] = True
                print(f"P{i} = True (Note: No resources allocated to P{i}, it cannot be part of a deadlock)")
            else:
                self.finish[i] = False
                print(f"P{i} = False")
        print(f"{'-'*40}")

    def run_detection(self):
        self.explain_initialization()
        
        step_count = 1
        processes_to_check = [i for i in range(self.n_processes) if not self.finish[i]]
        
        while True:
            found_process = False
            
            for i in range(self.n_processes):
                if not self.finish[i]:
                    print(f"\n{Colors.BOLD}{Colors.YELLOW}STEP {step_count}{Colors.ENDC}")
                    print(f"Checking Process {Colors.BOLD}P{i}{Colors.ENDC}")
                    
                    req = self.request[i]
                    can_execute = np.all(req <= self.work)
                    
                    print(f"\nCondition:")
                    print(f"Request[P{i}] <= Work")
                    print(f"{req.tolist()} <= {self.work.tolist()}")
                    
                    print(f"\nResult:")
                    if can_execute:
                        print(f"{Colors.GREEN}TRUE{Colors.ENDC}")
                        print(f"\n{Colors.BOLD}Teacher's Logic:{Colors.ENDC}")
                        print(f"Process P{i} is requesting resources that the system currently has available.")
                        print(f"Therefore, P{i} can complete its execution and release its currently held resources.")
                        
                        # Release resources
                        print(f"\nResources released by P{i}:")
                        print(f"Allocation[P{i}] = {self.allocation[i].tolist()}")
                        
                        old_work = self.work.copy()
                        self.work += self.allocation[i]
                        self.finish[i] = True
                        self.safe_sequence.append(f"P{i}")
                        
                        print(f"\nUpdated Work:")
                        print(f"Work = Work + Allocation[P{i}]")
                        print(f"{old_work.tolist()} + {self.allocation[i].tolist()}")
                        print(f"= {Colors.CYAN}{self.work.tolist()}{Colors.ENDC}")
                        
                        print(f"\nUpdated Finish Array:")
                        self.print_finish_status()
                        
                        remaining = [f"P{j}" for j in range(self.n_processes) if not self.finish[j]]
                        print(f"\nRemaining Processes: {remaining if remaining else 'None'}")
                        
                        found_process = True
                        step_count += 1
                        break 
                    else:
                        print(f"{Colors.RED}FALSE{Colors.ENDC}")
                        print(f"\n{Colors.BOLD}Teacher's Logic:{Colors.ENDC}")
                        print(f"Process P{i} is requesting more resources than currently available in 'Work'.")
                        print(f"P{i} must wait. Moving to check next process.")
                        
                        deadlocked_so_far = [f"P{j}" for j in range(self.n_processes) if not self.finish[j]]
                        print(f"Current Potential Deadlock Group: {deadlocked_so_far}")
            
            if not found_process:
                break
        
        self.conclude()

    def print_finish_status(self):
        status_str = ", ".join([f"P{i}={val}" for i, val in enumerate(self.finish)])
        print(status_str)

    def conclude(self):
        self.deadlocked_processes = [i for i in range(self.n_processes) if not self.finish[i]]
        is_deadlocked = len(self.deadlocked_processes) > 0
        
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*50}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}               FINAL RESULT{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*50}{Colors.ENDC}")
        
        if not is_deadlocked:
            print(f"\n{Colors.GREEN}{Colors.BOLD}SYSTEM STATE: SAFE / NO DEADLOCK{Colors.ENDC}")
            print(f"Safe Sequence: {' -> '.join(self.safe_sequence)}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}SYSTEM STATE: DEADLOCK DETECTED{Colors.ENDC}")
            print(f"Deadlocked Processes: {self.deadlocked_processes}")
        
        print(f"\nFinal Work Vector: {self.work.tolist()}")
        print(f"Final Finish Array: {self.finish.tolist()}")
        
        print(f"\n{Colors.BOLD}Algorithm Logic Summary:{Colors.ENDC}")
        print("1. Work is initialized to Available resources.")
        print("2. Finish[i] is False if process i has any allocation, True otherwise.")
        print("3. We search for an index i such that Finish[i] == False and Request[i] <= Work.")
        print("4. If found, we 'execute' the process, release its resources (Work = Work + Allocation), and set Finish[i] = True.")
        print("5. If no such i exists and some Finish[i] are still False, those processes are deadlocked.")
        
        print(f"\n{Colors.BOLD}Time Complexity Analysis:{Colors.ENDC}")
        print(f"O(m * n^2) where n is number of processes and m is number of resource types.")
        print("In each pass, we may check up to n processes. We may need up to n passes.")
        print("Each comparison takes O(m) time.")

def get_user_input():
    print(f"{Colors.BOLD}Deadlock Detection Input Configuration{Colors.ENDC}")
    try:
        n_p = int(input("Enter number of processes: "))
        n_r = int(input("Enter number of resource types: "))
        
        print("\nEnter Allocation Matrix (row by row):")
        alloc = []
        for i in range(n_p):
            row = list(map(int, input(f"  P{i}: ").split()))
            alloc.append(row)
            
        print("\nEnter Request Matrix (row by row):")
        req = []
        for i in range(n_p):
            row = list(map(int, input(f"  P{i}: ").split()))
            req.append(row)
            
        print("\nEnter Available Vector:")
        avail = list(map(int, input("  Available: ").split()))
        
        return n_p, n_r, alloc, req, avail
    except Exception as e:
        print(f"{Colors.RED}Error in input: {e}{Colors.ENDC}")
        sys.exit(1)

def run_sample():
    # Sample data from standard OS textbooks (e.g., Galvin)
    # 5 processes, 3 resources
    n_p = 5
    n_r = 3
    alloc = [
        [0, 1, 0], # P0
        [2, 0, 0], # P1
        [3, 0, 3], # P2
        [2, 1, 1], # P3
        [0, 0, 2]  # P4
    ]
    req = [
        [0, 0, 0], # P0
        [2, 0, 2], # P1
        [0, 0, 0], # P2
        [1, 0, 0], # P3
        [0, 0, 2]  # P4
    ]
    avail = [0, 0, 0]
    
    print(f"{Colors.BLUE}Running with built-in Sample Case...{Colors.ENDC}")
    sim = DeadlockSimulator(n_p, n_r, alloc, req, avail)
    sim.run_detection()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--sample":
        run_sample()
    else:
        print(f"{Colors.BOLD}Welcome to the Deadlock Detection Simulator{Colors.ENDC}")
        choice = input("Run sample case? (y/n): ").lower()
        if choice == 'y':
            run_sample()
        else:
            n_p, n_r, alloc, req, avail = get_user_input()
            sim = DeadlockSimulator(n_p, n_r, alloc, req, avail)
            sim.run_detection()
