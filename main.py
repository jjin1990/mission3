def mac(pattern, filter_):
    n = len(pattern)
    total = 0
    for i in range(n):
        for j in range(n):
            total = total + pattern[i][j] * filter_[i][j]
    return total

x_pattern = [[1,0,1], [0,1,0], [1,0,1]]
x_filter = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
cross_filter = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]

print(mac(x_pattern, x_filter))
print(mac(x_pattern, cross_filter))

