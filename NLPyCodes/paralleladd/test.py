import numpy as np

# 데이터 설정 (예시)
table1 = np.array([
    [1, 3, 4, 10],  # 영1
    [5, 4, 10, 1],  # 영2
    [14, 2, 5, 2]   # 영3
])

comp_mov = np.array([1, 5, 7, 7])

# 🚀 벡터 연산 (브로드캐스팅)
# table1의 모든 행에서 comp_mov를 뺀 뒤 절댓값을 구함
difference_abs = np.abs(table1 - comp_mov)

print("--- 뺄셈 후 절댓값 결과 (Difference Absolute) ---")
print(difference_abs)