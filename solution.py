n = int(input())
elements = list(map(int, input().split()))

results = []

for step in range(n):
    if step <= 1:
        # If we have 2 or fewer elements, max power is 0
        results.append(0)
        continue
    
    current_array = elements[:step + 1]
    array_len = len(current_array)
    
    # Precompute prefix minimums (min from left)
    prefix_min = [float('inf')] * array_len
    prefix_min[0] = current_array[0]
    for i in range(1, array_len):
        prefix_min[i] = min(prefix_min[i-1], current_array[i])
    
    # Precompute suffix maximums (max from right)
    suffix_max = [float('-inf')] * array_len
    suffix_max[array_len-1] = current_array[array_len-1]
    for i in range(array_len-2, -1, -1):
        suffix_max[i] = max(suffix_max[i+1], current_array[i])
    
    max_power = 0
    
    # Calculate power for each middle element
    for i in range(1, array_len - 1):
        min_left = prefix_min[i-1]
        max_right = suffix_max[i+1]
        power = max_right - min_left
        max_power = max(max_power, power)
    
    results.append(max_power)

# Output results
print(' '.join(map(str, results)))