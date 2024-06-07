import pandas as pd

normal_file_path='./CSV/normal.csv'

# 음식점 데이터 로드
normal = pd.read_csv(normal_file_path, encoding="CP949")
print(normal)
deleteAfterRow = normal[normal['영업상태명'] == '폐업'].index
reslut = normal.drop(deleteAfterRow)
reslut.to_csv('updateNormal.csv')
print(reslut)