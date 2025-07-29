def can_give_length(worms, k, length):
    """Проверяет, можно ли получить k кусочков длины length из червячков"""
    if length == 0:
        return True
    
    count = 0
    for worm_length in worms:
        count += worm_length // length
        if count >= k:
            return True
    return count >= k

def solve():
    # Читаем входные данные
    n, k = map(int, input().split())
    worms = list(map(int, input().split()))
    
    # Бинарный поиск по длине
    left = 0
    right = max(worms)
    
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        
        if can_give_length(worms, k, mid):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    print(answer)

if __name__ == "__main__":
    solve()