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

def select_mode():
    print("=== Mini NPU Simulator ===")
    print()
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    while True:
        text = input("선택: ").strip()
        if text == "1":
            return "1"
        elif text == "2":
            return "2"
        else:
            print("1 또는 2를 입력하세요.")

ERROR_MSG = "입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요."

def read_row(n):
    while True:
        parts = input().split()
        if len(parts) != n:
            print(ERROR_MSG)
            continue
        try:
            row = []
            for p in parts:
                row.append(float(p))
        except ValueError:
            print(ERROR_MSG)
            continue
        return row

def read_matrix(n, title):
    print(title, "(" + str(n) + "줄 입력, 공백 구분)")
    matrix = []
    for i in range(n):
        matrix.append(read_row(n))
    return matrix

x_pattern = [[1,0,1], [0,1,0], [1,0,1]]
x_filter = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
cross_filter = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]

print(mac(x_pattern, x_filter))
print(mac(x_pattern, cross_filter))

print(judge(5, 1, "A", "B"))
print(judge(3, 5, "A", "B"))
print(judge(0.9, 0.8999999999999999, "A", "B"))

#print(select_mode())

#print(read_row(3))

print(read_matrix(3, "필터 A"))
