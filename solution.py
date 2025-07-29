def solve():
    n = int(input())
    elements = list(map(int, input().split()))
    
    result = []
    
    for step in range(1, n + 1):
        if step <= 2:
            result.append(0)
            continue
        
        max_power = 0
        
        # Для каждого элемента (кроме крайних) вычисляем его мощность
        for i in range(1, step - 1):
            # Минимальный элемент слева от позиции i
            min_left = min(elements[:i])
            # Максимальный элемент справа от позиции i  
            max_right = max(elements[i + 1:step])
            
            # Мощность элемента на позиции i
            power = max_right - min_left
            max_power = max(max_power, power)
        
        result.append(max_power)
    
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    solve()