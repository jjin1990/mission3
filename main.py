import time

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

def measure_ms(pattern,filter_, repeat=10):
    start = time.perf_counter()
    for _ in range(repeat):
        mac(pattern, filter_)
    end = time.perf_counter()
    return (end - start) * 1000 / repeat

def run_mode1():
    filter_a = read_matrix(3, "필터 A")
    filter_b = read_matrix(3, "필터 B")
    pattern = read_matrix(3, "패턴")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    result = judge(score_a, score_b, "A", "B")

    print("A 점수:", score_a)
    print("B 점수:", score_b)
    print("연산 시간(평균/10회):", round(measure_ms(pattern, filter_a), 3), "ms")
    if result == "UNDECIDED":
        print("판정: 판정 불가 (|A-B| < 1e-9)")
    else:
        print("판정:", result)
    
mode = select_mode()
if mode == "1":
    run_mode1()
else:
    print("모드 2는 준비 중입니다.")
