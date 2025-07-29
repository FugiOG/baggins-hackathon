n = int(input())
elements = list(map(int, input().split()))

results = []
max_power = 0

for step in range(n):
    if step <= 1:
        results.append(0)
        continue
    
    # When we add a new element at position 'step', we need to:
    # 1. Check if any existing middle elements get a new max power due to the new element
    # 2. The new element itself cannot be a middle element (it's the rightmost)
    
    new_element = elements[step]
    
    # Check all existing middle elements (positions 1 to step-1)
    for i in range(1, step):
        # For element at position i:
        # - min_left is from elements[0] to elements[i-1] 
        # - max_right is from elements[i+1] to elements[step] (including new element)
        
        min_left = min(elements[j] for j in range(i))
        max_right = max(elements[j] for j in range(i + 1, step + 1))
        
        power = max_right - min_left
        max_power = max(max_power, power)
    
    results.append(max_power)

print(' '.join(map(str, results)))