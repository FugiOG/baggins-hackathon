n = int(input())
a = list(map(int, input().split()))

result = []
global_max_power = 0

for step in range(n):
    if step <= 1:
        result.append(0)
        continue
    
    # Поддерживаем глобальный максимум мощности
    step_max_power = 0
    
    # Вычисляем префиксные минимумы для текущего массива
    min_prefix = [0] * (step + 1)
    min_prefix[0] = a[0]
    for i in range(1, step + 1):
        min_prefix[i] = min(min_prefix[i-1], a[i])
    
    # Вычисляем суффиксные максимумы эффективно - справа налево
    max_suffix = a[step]
    
    # Идем по средним позициям справа налево
    for i in range(step - 1, 0, -1):
        # Для позиции i: min_left от min_prefix[i-1], max_right это max_suffix
        min_left = min_prefix[i - 1]
        max_right = max_suffix
        power = max_right - min_left
        step_max_power = max(step_max_power, power)
        
        # Обновляем max_suffix для следующей итерации
        max_suffix = max(max_suffix, a[i])
    
    # Глобальный максимум может только расти
    global_max_power = max(global_max_power, step_max_power)
    result.append(global_max_power)

print(' '.join(map(str, result)))