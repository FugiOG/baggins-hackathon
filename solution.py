n = int(input())
a = list(map(int, input().split()))

result = []
max_power = 0

# Precompute all prefix minimums once - O(n)
prefix_min = [0] * n
prefix_min[0] = a[0]
for i in range(1, n):
    prefix_min[i] = min(prefix_min[i-1], a[i])

for step in range(n):
    if step <= 1:
        result.append(0)
        continue
    
    # For current array a[0..step], we need max power of middle elements a[1..step-1]
    step_max = 0
    
    # Use efficient suffix maximum computation
    # For each middle position i, we need max(a[i+1..step])
    suffix_max = a[step]  # Start from rightmost
    
    # Go backwards from step-1 to 1 (all possible middle positions)
    for i in range(step-1, 0, -1):
        # For middle position i, max_right is current suffix_max
        min_left = prefix_min[i-1]
        max_right = suffix_max
        power = max_right - min_left
        step_max = max(step_max, power)
        
        # Update suffix_max to include a[i] for next iteration
        suffix_max = max(suffix_max, a[i])
    
    max_power = max(max_power, step_max)
    result.append(max_power)

print(' '.join(map(str, result)))