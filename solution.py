from collections import deque

n = int(input())
elements = list(map(int, input().split()))

results = []

for step in range(n):
    if step <= 1:
        results.append(0)
        continue
    
    current_len = step + 1
    max_power = 0
    
    # For current array of length current_len
    # We need to find max power among all middle elements (indices 1 to current_len-2)
    
    # Precompute prefix minimums efficiently
    prefix_min = [0] * current_len
    prefix_min[0] = elements[0]
    for i in range(1, current_len):
        prefix_min[i] = min(prefix_min[i-1], elements[i])
    
    # Precompute suffix maximums efficiently
    suffix_max = [0] * current_len
    suffix_max[current_len-1] = elements[current_len-1]
    for i in range(current_len-2, -1, -1):
        suffix_max[i] = max(suffix_max[i+1], elements[i])
    
    # Calculate power for each middle element
    for i in range(1, current_len - 1):
        min_left = prefix_min[i-1]
        max_right = suffix_max[i+1]
        power = max_right - min_left
        max_power = max(max_power, power)
    
    results.append(max_power)

print(' '.join(map(str, results)))