import sys

# Set the desired recursion depth limit
new_recursion_limit = 10000  # Change this to the desired limit

try:
    sys.setrecursionlimit(new_recursion_limit)
    print("New Recursion Limit Set")
except Exception as e:
    print(f"Setting recursion limit failed: {e}")
