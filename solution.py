import sys


input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

# Добавьте сюда решение задачи

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

# Бинарный поиск по длине
left = 0
right = max(a)

answer = 0

while left <= right:
    mid = (left + right) // 2
    
    if can_give_length(a, k, mid):
        answer = mid
        left = mid + 1
    else:
        right = mid - 1

print(answer)