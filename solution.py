n = int(input())
a = list(map(int, input().split()))

result = [0] * n

if n <= 2:
    print(' '.join(map(str, result)))
else:
    max_power = 0
    
    for k in range(2, n):
        # At step k, we have array a[0..k]
        # Find max power among middle elements a[1..k-1]
        
        # Use optimized approach: precompute what we need
        min_prefix = [0] * k
        min_prefix[0] = a[0]
        for i in range(1, k):
            min_prefix[i] = min(min_prefix[i-1], a[i])
        
        max_suffix = [0] * (k + 1)
        max_suffix[k] = a[k]
        for i in range(k-1, 1, -1):
            max_suffix[i] = max(max_suffix[i+1], a[i])
        
        # Check all middle positions
        for i in range(1, k):
            power = max_suffix[i+1] - min_prefix[i-1]
            max_power = max(max_power, power)
        
        result[k] = max_power
    
    print(' '.join(map(str, result)))