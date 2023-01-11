def solution(A):
    # Implement your solution here
    N = len(A)
    dict = {}

    for i in A:
        if i > 0:
            dict.update({i:1})
    for i in range(1, N+2):
        if i not in dict:
            return i;
  

print(solution([-1,-3]))