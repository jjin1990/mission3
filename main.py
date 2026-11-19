def mac(pattern, filter_):
    n = len(pattern)
    total = 0
    for i in range(n):
        for j in range(n):
            total = total + pattern[i][j] * filter_[i][j]
    return total

EPSILON = 1e-9

def judge(score_a, score_b, name_a, name_b):
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    elif score_a > score_b:
        return name_a
    else:
        return name_b

x_pattern = [[1,0,1], [0,1,0], [1,0,1]]
x_filter = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
cross_filter = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]

print(mac(x_pattern, x_filter))
print(mac(x_pattern, cross_filter))

print(judge(5, 1, "A", "B"))
print(judge(3, 5, "A", "B"))
print(judge(0.9, 0.8999999999999999, "A", "B"))