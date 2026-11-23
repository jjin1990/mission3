import time
import json

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
    print("필터 A, B 저장 완료")
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

def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_label(text):
    t = str(text).strip().lower()
    if t == "+" or t == "cross":
        return "Cross"
    elif t == "x":
        return "X"
    else:
        return None


def size_from_key(key):
    return int(key.split("_")[1])


def is_square(matrix, n):
    if len(matrix) != n:
        return False
    for row in matrix:
        if len(row) != n:
            return False
    return True

def make_cross(n):
    mid = n // 2
    pattern = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == mid or j == mid:
                row.append(1.0)
            else:
                row.append(0.0)
        pattern.append(row)
    return pattern

def make_x(n):
    pattern = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j or i + j == n - 1:
                row.append(1.0)
            else:
                row.append(0.0)
        pattern.append(row)
    return pattern

def print_performance(filters):
    print("크기\t평균 시간(ms)\t연산 횟수")
    print("-" * 37)
    for n in [3, 5, 13, 25]:
        p = make_x(n)
        f = make_cross(n)
        ms = measure_ms(p, f)
        print(str(n) + "×" + str(n), "\t", round(ms, 3), "\t\t", n * n)


def run_mode2():
    try:
        data = load_data("data.json")
    except (FileNotFoundError, json.JSONDecodeError):
        print("data.json을 읽을 수 없습니다.")
        return

    print("# [1] 필터 로드")
    filters = {}
    for size_key, pair in data["filters"].items():
        n = size_from_key(size_key)
        filters[n] = {}
        for label, matrix in pair.items():
            filters[n][normalize_label(label)] = matrix
        print("✓", size_key, "필터 로드 완료 (Cross, X)")

    print()
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    total = 0
    passed = 0
    fails = []
    for key, case in data["patterns"].items():
        total = total + 1
        print("---", key, "---")
        try:
            n = size_from_key(key)
            pattern = case["input"]
            expected = normalize_label(case["expected"])
        except (KeyError, ValueError, IndexError, TypeError):
            print("FAIL (데이터 형식 오류)")
            fails.append(key + ": 데이터 형식 오류(키·input·expected 확인)")
            continue
        if n not in filters:
            print("FAIL (size_" + str(n) + " 필터 없음)")
            fails.append(key + ": size_" + str(n) + " 필터 없음")
            continue
        if not is_square(pattern, n):
            print("FAIL (크기 불일치)")
            fails.append(key + ": 패턴 크기가 " + str(n) + "×" + str(n) + "이 아님")
            continue
        score_cross = mac(pattern, filters[n]["Cross"])
        score_x = mac(pattern, filters[n]["X"])
        result = judge(score_cross, score_x, "Cross", "X")
        print("Cross 점수:", score_cross)
        print("X 점수:", score_x)
        if result == expected:
            passed = passed + 1
            print("판정:", result, "| expected:", expected, "| PASS")
        else:                                           # 다르면
            print("판정:", result, "| expected:", expected, "| FAIL")
            if result == "UNDECIDED":
                fails.append(key + ": 동점(UNDECIDED) 처리 규칙에 따라 FAIL")
            else:
                fails.append(key + ": 판정 " + result + "이 expected " + str(expected) + "와 다름")

    print()
    print("# [3] 성능 분석 (평균/10회)")
    print_performance(filters)

    print()
    print("# [4] 결과 요약")
    print("총 테스트:", total, "개")
    print("통과:", passed, "개")
    print("실패:", len(fails), "개")
    if len(fails) > 0:
        print()
        print("실패 케이스:")
        for f in fails:
            print("-", f)
    
mode = select_mode()
if mode == "1":
    run_mode1()
else:
    run_mode2()
