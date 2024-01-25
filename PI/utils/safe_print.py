import threading

print_lock = threading.Lock()

def safe_print(*args):
    with print_lock:
        for arg in args:  # arg is one line
            print(arg) 